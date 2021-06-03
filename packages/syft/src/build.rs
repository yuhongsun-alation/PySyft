use prost_build;
use std::path::Path;
use std::process::Command;
use walkdir;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let files: Vec<_> = walkdir::WalkDir::new("../proto")
        .into_iter()
        .filter_map(|dir_entry| {
            dir_entry.ok().and_then(|entry| {
                if entry.file_type().is_dir() {
                    None
                } else {
                    if entry.file_name().to_str().unwrap().ends_with(".proto") {
                        Some(entry.path().to_owned())
                    } else {
                        None
                    }
                }
            })
        })
        .collect();
    let mut prost_build = prost_build::Config::new();
    prost_build.protoc_arg("--experimental_allow_proto3_optional");
    prost_build.compile_protos(&files, &[Path::new("../").to_path_buf()])?;

    // syft-core protos
    let output = if cfg!(target_os = "windows") {
        Command::new("cmd")
            .args(&["/C", "echo hello"])
            .output()
            .expect("failed to execute process")
    } else {
        Command::new("sh")
            .arg("-c")
            .arg("protoc -I=../../proto/syft-core --python_out=./syft/proto ../../proto/syft-core/message.proto")
            .output()
            .expect("failed to execute process")
    };

    println!("out: {:?}", output);

    Ok(())
}
