# 🤖 Warehouse Cleanup Robot Simulation

An autonomous warehouse cleanup robot simulation using ROS 2, Gazebo, SLAM Toolbox, and a LiDAR camera. The robot patrols a messy warehouse floor, detects displaced boxes, and returns them to designated storage zones.

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running the Simulation](#running-the-simulation)
- [Cleanup Pipeline](#cleanup-pipeline)
- [SLAM & Navigation](#slam--navigation)
- [LiDAR Camera Integration](#lidar-camera-integration)
- [Topics & Services](#topics--services)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project simulates an autonomous mobile robot (AMR) operating inside a warehouse with randomly displaced boxes scattered across the floor. The robot navigates using SLAM (Simultaneous Localization and Mapping), detects displaced boxes via a LiDAR camera, scoops them up with a forklift attachment, and deposits them in designated storage zones.

The simulation environment is built in Gazebo and the entire software stack runs on ROS 2 (Humble / Iron).

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        ROS 2 Stack                          │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  LiDAR Cam   │───▶│  SLAM        │───▶│  Nav2        │  │
│  │  (Perception)│    │  Toolbox     │    │  Planner     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                                        │          │
│         ▼                                        ▼          │
│  ┌──────────────┐                        ┌──────────────┐  │
│  │  Box         │                        │  Robot       │  │
│  │  Detector    │───────────────────────▶│  Controller  │  │
│  └──────────────┘                        └──────────────┘  │
│                                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
              ┌─────────▼─────────┐
              │      Gazebo       │
              │    Simulation     │
              └───────────────────┘
```

---

## Features

- Warehouse floor environment in Gazebo with randomly spawned displaced boxes
- Forklift-style robot with a single lift joint for box retrieval
- Autonomous navigation powered by Nav2
- Real-time map building with SLAM Toolbox
- LiDAR point cloud processing for floor-level box detection
- State machine managing patrol, detect, retrieve, and deposit behaviors
- Configurable storage zones for cleaned-up boxes
- RViz2 visualization for live map, robot pose, and sensor feeds
- Reproducible box spawn patterns via random seed

---

## Prerequisites

| Dependency | Version | Notes |
|---|---|---|
| Ubuntu | 22.04 LTS | Recommended OS |
| ROS 2 | Humble Hawksbill | LTS release |
| Gazebo | Fortress (11) | Classic or Ignition |
| Python | 3.10+ | For perception nodes |
| SLAM Toolbox | Latest | `apt install` |
| Nav2 | Latest | Navigation stack |
| PCL | 1.12+ | LiDAR processing |
| OpenCV | 4.x | Image processing |

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/warehouse-cleanup-robot-sim.git
cd warehouse-cleanup-robot-sim
```

### 2. Install ROS 2 Dependencies

```bash
sudo apt update && sudo apt install -y \
  ros-humble-slam-toolbox \
  ros-humble-nav2-bringup \
  ros-humble-navigation2 \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros2-control \
  ros-humble-robot-state-publisher \
  ros-humble-joint-state-publisher \
  ros-humble-pcl-ros \
  ros-humble-sensor-msgs \
  ros-humble-vision-msgs \
  python3-colcon-common-extensions
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Build the Workspace

```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

---

## Project Structure

```
warehouse-cleanup-robot-sim/
├── src/
│   ├── warehouse_description/       # Robot URDF & meshes
│   │   ├── urdf/
│   │   │   ├── robot.urdf.xacro
│   │   │   └── sensors/
│   │   │       └── lidar_camera.xacro
│   │   └── meshes/
│   ├── warehouse_gazebo/            # Simulation world & launch files
│   │   ├── worlds/
│   │   │   └── warehouse_floor.world
│   │   ├── models/
│   │   │   ├── boxes/
│   │   │   └── storage_zones/
│   │   └── launch/
│   │       └── warehouse_sim.launch.py
│   ├── warehouse_slam/              # SLAM configuration & launch
│   │   ├── config/
│   │   │   └── slam_toolbox_params.yaml
│   │   └── launch/
│   │       └── slam.launch.py
│   ├── warehouse_navigation/        # Nav2 configuration
│   │   ├── config/
│   │   │   ├── nav2_params.yaml
│   │   │   └── costmap_params.yaml
│   │   └── launch/
│   │       └── navigation.launch.py
│   ├── box_perception/              # LiDAR-based box detection
│   │   ├── box_perception/
│   │   │   ├── lidar_processor.py
│   │   │   ├── box_detector.py
│   │   │   └── storage_router.py
│   │   └── config/
│   │       └── detector_params.yaml
│   ├── robot_state_machine/         # Patrol / detect / retrieve / deposit
│   │   └── cleanup_state_machine.py
│   └── warehouse_bringup/           # Top-level launch files
│       └── launch/
│           └── full_simulation.launch.py
├── maps/
│   └── warehouse_map.yaml
├── scripts/
│   ├── spawn_boxes.py
│   └── visualize_zones.py
├── requirements.txt
├── package.xml
└── README.md
```

---

## Configuration

### SLAM Toolbox (`slam_toolbox_params.yaml`)

```yaml
slam_toolbox:
  ros__parameters:
    solver_plugin: solver_plugins::CeresSolver
    ceres_linear_solver: SPARSE_NORMAL_CHOLESKY
    mode: mapping                   # Use 'localization' on known maps
    map_update_interval: 5.0
    max_laser_range: 20.0
    resolution: 0.05
    minimum_travel_distance: 0.5
    minimum_travel_heading: 0.5
    scan_buffer_size: 10
    loop_search_maximum_distance: 3.0
    do_loop_closing: true
```

### LiDAR Camera Parameters (`detector_params.yaml`)

```yaml
lidar_processor:
  ros__parameters:
    point_cloud_topic: /lidar_camera/points
    min_cluster_size: 50
    max_cluster_size: 5000
    cluster_tolerance: 0.05         # 5 cm Euclidean distance
    voxel_leaf_size: 0.02           # Downsampling resolution
    ground_removal_threshold: 0.15  # Meters above ground

box_detector:
  ros__parameters:
    detection_height_max: 0.6       # Only detect floor-level objects
    storage_zones:
      zone_a: [5.0, 2.0]
      zone_b: [5.0, -2.0]
```

---

## Running the Simulation

### Full Simulation (All-in-One)

```bash
source install/setup.bash
ros2 launch warehouse_bringup full_simulation.launch.py
```

### Step-by-Step Launch

```bash
# Terminal 1 — Gazebo world + robot
ros2 launch warehouse_gazebo warehouse_sim.launch.py

# Terminal 2 — SLAM
ros2 launch warehouse_slam slam.launch.py

# Terminal 3 — Navigation
ros2 launch warehouse_navigation navigation.launch.py

# Terminal 4 — Box Perception + State Machine
ros2 run box_perception box_detector
ros2 run robot_state_machine cleanup_state_machine

# Terminal 5 — RViz2
rviz2 -d config/warehouse.rviz
```

### Spawn Boxes into the World

```bash
python3 scripts/spawn_boxes.py --count 20 --random-seed 42
```

---

## Cleanup Pipeline

The robot operates on a continuous four-stage loop:

1. **Patrol** — The robot roams the warehouse floor using a coverage pattern
2. **Detect** — The LiDAR camera publishes a PointCloud2 stream; the `box_detector` node applies ground removal and Euclidean clustering to identify displaced boxes on the floor
3. **Retrieve** — The robot navigates to the detected box and scoops it using the forklift lift joint
4. **Deposit** — The robot navigates to the nearest storage zone and lowers the fork to deposit the box, then returns to patrol

```
Patrol ──▶ Detect Box ──▶ Navigate to Box ──▶ Lift Fork
                                                   │
                                         Navigate to Storage Zone
                                                   │
                                            Lower Fork / Deposit
                                                   │
                                            Return to Patrol ◀──
```

---

## SLAM & Navigation

The robot builds a 2D occupancy grid map using SLAM Toolbox while simultaneously localizing itself within it. LiDAR scan data is fused with odometry to produce a consistent global map.

Once mapping is complete, save the map with:

```bash
ros2 run nav2_map_server map_saver_cli -f maps/warehouse_map
```

Switch SLAM Toolbox to localization mode for subsequent runs:

```yaml
# slam_toolbox_params.yaml
mode: localization
map_file_name: /path/to/maps/warehouse_map
```

Nav2 handles global path planning (NavFn), local trajectory control (DWB), and recovery behaviors (spin, back-up, wait).

---

## LiDAR Camera Integration

The simulation uses a combined LiDAR + RGB-D camera sensor mounted on the robot's front chassis.

| Topic | Type | Description |
|---|---|---|
| `/lidar_camera/points` | `sensor_msgs/PointCloud2` | 3D point cloud |
| `/lidar_camera/scan` | `sensor_msgs/LaserScan` | 2D scan slice for SLAM |
| `/lidar_camera/image_raw` | `sensor_msgs/Image` | RGB image |
| `/lidar_camera/depth/image_raw` | `sensor_msgs/Image` | Depth image |

---

## Topics & Services

### Subscribed Topics

| Topic | Type | Node |
|---|---|---|
| `/lidar_camera/points` | `PointCloud2` | `box_detector` |
| `/odom` | `nav_msgs/Odometry` | SLAM, Nav2 |
| `/tf`, `/tf_static` | `tf2_msgs/TFMessage` | All nodes |

### Published Topics

| Topic | Type | Node |
|---|---|---|
| `/map` | `nav_msgs/OccupancyGrid` | SLAM Toolbox |
| `/detected_boxes` | `vision_msgs/Detection3DArray` | `box_detector` |
| `/cmd_vel` | `geometry_msgs/Twist` | Nav2 controller |
| `/robot_status` | `std_msgs/String` | `cleanup_state_machine` |

### Services

| Service | Type | Description |
|---|---|---|
| `/slam_toolbox/save_map` | `slam_toolbox/SaveMap` | Persist the current map |
| `/cleanup/reset` | `std_srvs/Trigger` | Reset cleanup state |
| `/storage_router/get_status` | `std_srvs/Trigger` | Query deposit queue |

---

## Troubleshooting

### Gazebo crashes on launch
Make sure `GAZEBO_MODEL_PATH` includes the project models directory:

```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$(pwd)/src/warehouse_gazebo/models
```

### SLAM map is drifting
Reduce the robot's maximum speed in `nav2_params.yaml` and ensure the LiDAR scan topic matches the SLAM Toolbox configuration (`scan_topic` parameter).

### No point cloud published
Verify the LiDAR plugin is loaded in Gazebo:

```bash
ros2 topic echo /lidar_camera/points --no-arr
```

If no messages appear, check the sensor plugin tag in `lidar_camera.xacro`.

### Boxes clipping through the floor on spawn
The spawn script places boxes with a small Z offset. If you still see physics issues, increase `spawn_z_offset` in `spawn_boxes.py`.

### Nav2 goal rejected
Ensure the costmap has finished inflating after the map loads. Add a short sleep before publishing goals in automation scripts.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please follow the ROS 2 code style guidelines and include unit tests for new nodes.

---

## License

This project is licensed under the Apache 2.0 License — see the [LICENSE](LICENSE) file for details.

---

*Built with ROS 2 Humble · Gazebo Fortress · SLAM Toolbox · Nav2 · PCL*
