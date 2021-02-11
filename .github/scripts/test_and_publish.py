#!/usr/bin/env python3

import subprocess, sys, os, tempfile
from distantrs import Invocation
from glob import glob

INVOCATION_DATA_PATH = os.path.join(
        tempfile.gettempdir(),
        'distant-rs-invocation.txt'
        )

# required to find listener.py
this_path = os.path.abspath(os.path.dirname(__file__))
test_script_path = f"{os.environ.get('GITHUB_WORKSPACE')}/renode/test.sh"
inv_data_str = ""
robot_name = sys.argv[1].split(".")[0]

try:
    with open(INVOCATION_DATA_PATH, 'r') as f:
        inv_data_str = f.read()
except IOError:
    print(str(e))
    sys.exit(1)

inv_data_lst = inv_data_str.split("--")

i = Invocation(
        invocation_id=inv_data_lst[0],
        auth_token=inv_data_lst[1]
        )

i.announce_target(robot_name)

tmp = tempfile.NamedTemporaryFile()
with open(tmp.name, 'w') as log:
    # run the actual testing procedure
    subprocess_args = [
            test_script_path, 
            "--listener",
            os.path.join(this_path, f"results_listener.py:{inv_data_str}"),
            sys.argv[1],
    ]

    process = subprocess.Popen(
        subprocess_args,
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        env=os.environ.copy()
        )

    ret = 0

    while True:
        line = process.stdout.readline().decode('utf-8').rstrip()
        ret = process.poll()
        if ret is not None:
            break
        if line:
            log.write(f'{line}\n')
            print(line)


i.add_log_to_target(
    target_name=robot_name,
    log_path=tmp.name
    )

dumps = glob('*.dump')

expected_artifact_paths = [
        'robot_output.xml',
        'log.html',
        'report.html',
        ]
expected_artifact_paths.extend(dumps)

existing_artifact_paths = [x for x in expected_artifact_paths if os.path.isfile(x)]

for path in existing_artifact_paths:
    i.send_file_target(
        target_name=robot_name,
        file_name=os.path.basename(path),
        file_path=path
        )

# If the tests failed, mark the target as failed and exit.
if ret != 0:
    i.finalize_target(
        name=robot_name, 
        success=not(ret)
        )
    sys.exit(ret)

# Run the metrics analyzer for each dump file and upload it.
for dump_file in dumps:
    dump_file_target = dump_file.split(".")[0]

    graph_directory = f'{dump_file_target}_graphs'
    os.makedirs(graph_directory)

    v_args = [
            'python',
            f'{os.environ["GITHUB_WORKSPACE"]}/{os.environ["METRICS_VISUALIZER"]}',
            dump_file,
            '--no-dialogs',
            '-o',
            graph_directory
    ]
    v_process = subprocess.Popen(v_args)
    v_process.communicate()

    if v_process.returncode == 0:
        graph_files = glob(f'{graph_directory}/*.png')
        
        for graph_f in graph_files:
            i.send_file_target(
                    target_name=robot_name,
                    file_name=f'{dump_file_target}_{os.path.basename(graph_f)}',
                    file_path=graph_f
                    )
        
    
i.finalize_target(
    name=robot_name, 
    success=not(ret)
    )
