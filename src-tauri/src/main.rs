// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::collections::HashMap;
use std::path::PathBuf;
use tauri::api::process::{Command, CommandEvent};
use tauri::async_runtime::Receiver;
use tauri::{App, Manager, Window};

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let rx = spawn_ui(app);
            let main_window = app.get_window("main").unwrap();
            listen_ui_std(rx, main_window);
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

fn spawn_ui(app: &mut App) -> Receiver<CommandEvent> {
    let resource_path = get_resource_path(app);

    let current_dir = get_current_dir(&resource_path);
    let old_path = get_old_env("PATH");
    let new_path = get_new_path(&current_dir, &old_path);

    let package_path = get_package_path(&resource_path);
    let mut envs = HashMap::new();
    envs.insert("PYTHONPATH".to_string(), package_path);
    envs.insert("PATH".to_string(), new_path);

    let python = get_python_exe(&current_dir);

    let (rx, _child) = Command::new(&python)
        .current_dir(PathBuf::from(&current_dir).parent().unwrap().parent().unwrap().to_path_buf())
        .args(&["main.py"])
        .envs(envs)
        .spawn()
        .unwrap_or_else(|e| {
            std::fs::write("./err.txt", format!("Failed to spawn sidecar: {}", e)).unwrap();
            std::fs::write("./resource_path.txt", resource_path).unwrap();
            std::fs::write("./current_dir.txt", current_dir).unwrap();
            std::fs::write("./python.txt", python).unwrap();
            panic!("Failed to spawn sidecar: {}", e);
        });
    rx
}

fn get_python_exe(current_dir: &String) -> String {
    let python = if cfg!(windows) {
        "python.exe"
    } else {
        "python"
    };
    let python = format!("{}/{}", current_dir, python);
    python
}

fn get_current_dir(resource_path: &String) -> String {
    let current_dir = if cfg!(windows) {
        format!("{}/{}", &resource_path, "env/Scripts".to_string())
    } else {
        format!("{}/{}", &resource_path, "env/bin".to_string())
    };
    current_dir
}

fn get_old_env(key: &str) -> String {
    std::env::var(key).unwrap_or("".to_string())
}

fn get_new_path(current_dir: &String, old_path: &String) -> String {
    let new_path = if cfg!(windows) {
        format!("{};{}", &old_path, &current_dir)
    } else {
        format!("{}:{}", &old_path, &current_dir)
    };
    new_path
}

fn listen_ui_std(mut rx: Receiver<CommandEvent>, main_window: Window) {
    tauri::async_runtime::spawn(async move {
        // read events such as stdout
        while let Some(event) = rx.recv().await {
            match event {
                CommandEvent::Stderr(line) => {
                    println!("Received stderr: {}", line);
                }
                CommandEvent::Stdout(line) => {
                    if line.contains(" Network URL: ") {
                        main_window
                            .eval("window.location.replace('http://localhost:7561')")
                            .expect(
                                "
                                failed to execute window.location.replace()",
                            );
                        println!("WebUI start successful");
                    } else {
                        println!("Received stdout: {}", line);
                    }
                }
                _ => {
                    println!("Received other event");
                }
            }
        }
    });
}

fn get_package_path(resource_path: &String) -> String {
    let old_package_path = get_old_env("PYTHONPATH");
    let package_path = if cfg!(windows) {
        format!(
            "{};{}{}",
            old_package_path,
            &resource_path,
            "/env/Lib/site-packages".to_string()
        )
    } else {
        format!(
            "{}:{}{}",
            old_package_path,
            &resource_path,
            "/env/lib/python3.9/site-packages".to_string()
        )
    };
    package_path
}

fn get_resource_path(app: &mut App) -> String {
    let resource_path = app
        .path_resolver()
        .resolve_resource("bin")
        .unwrap_or_else(|| {
            std::fs::write("./err.txt", "Failed to resolve resource path").unwrap();
            panic!("Failed to resolve resource path");
        })
        .to_str()
        .unwrap()
        .to_string();
    resource_path
}

// write a test
#[cfg(test)]
mod tests {
  use super::*;


  #[test]
  fn t1() {
      let path = &"".to_string();
      let string = get_package_path(path);
      println!("{}", string);
  }
}
