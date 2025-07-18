"""
Complete database schema extracted from actual database dumps
This provides comprehensive context for intelligent querying without SQL knowledge
"""

# Complete Pitching Database Schema
PITCHING_COMPLETE_SCHEMA = {
    "database_name": "theia_pitching_db",
    "description": "Complete biomechanical analysis for baseball pitching",
    
    "poi_metrics": {
        # Core Performance
        "pitch_speed_mph": "Ball velocity at release",
        
        # Rotational Velocities (Angular Velocities)
        "max_shoulder_internal_rotational_velo": "Peak shoulder rotation speed",
        "max_elbow_extension_velo": "Peak elbow extension speed", 
        "max_torso_rotational_velo": "Peak torso rotation speed",
        "max_pelvis_rotational_velo": "Peak pelvis rotation speed",
        "lead_knee_extension_angular_velo_fp": "Lead knee extension speed at foot plant",
        "lead_knee_extension_angular_velo_br": "Lead knee extension speed at ball release",
        "lead_knee_extension_angular_velo_max": "Maximum lead knee extension speed",
        
        # Joint Positions & Angles
        "max_rotation_hip_shoulder_separation": "Maximum separation between hips and shoulders",
        "max_elbow_flexion": "Maximum elbow bend angle",
        "max_shoulder_external_rotation": "Maximum shoulder external rotation",
        "max_shoulder_horizontal_abduction": "Maximum shoulder horizontal abduction",
        
        # Positions at Foot Plant (fp)
        "elbow_flexion_fp": "Elbow bend at foot plant",
        "elbow_pronation_fp": "Elbow pronation at foot plant", 
        "rotation_hip_shoulder_separation_fp": "Hip-shoulder separation at foot plant",
        "shoulder_horizontal_abduction_fp": "Shoulder horizontal abduction at foot plant",
        "shoulder_abduction_fp": "Shoulder abduction at foot plant",
        "shoulder_external_rotation_fp": "Shoulder external rotation at foot plant",
        "torso_anterior_tilt_fp": "Torso forward tilt at foot plant",
        "torso_lateral_tilt_fp": "Torso side tilt at foot plant",
        "torso_rotation_fp": "Torso rotation at foot plant",
        "pelvis_anterior_tilt_fp": "Pelvis forward tilt at foot plant",
        "pelvis_lateral_tilt_fp": "Pelvis side tilt at foot plant",
        "pelvis_rotation_fp": "Pelvis rotation at foot plant",
        
        # Positions at Maximum External Rotation (mer)
        "glove_shoulder_abduction_mer": "Glove shoulder abduction at max external rotation",
        "elbow_flexion_mer": "Elbow flexion at max external rotation",
        "torso_anterior_tilt_mer": "Torso anterior tilt at max external rotation",
        "torso_lateral_tilt_mer": "Torso lateral tilt at max external rotation", 
        "torso_rotation_mer": "Torso rotation at max external rotation",
        
        # Positions at Ball Release (br)
        "torso_anterior_tilt_br": "Torso anterior tilt at ball release",
        "torso_lateral_tilt_br": "Torso lateral tilt at ball release",
        "torso_rotation_br": "Torso rotation at ball release",
        "lead_knee_extension_from_fp_to_br": "Lead knee extension from foot plant to ball release",
        
        # Glove Side Metrics
        "glove_shoulder_horizontal_abduction_fp": "Glove shoulder horizontal abduction at foot plant",
        "glove_shoulder_abduction_fp": "Glove shoulder abduction at foot plant",
        "glove_shoulder_external_rotation_fp": "Glove shoulder external rotation at foot plant",
        
        # Kinetic Chain & Timing
        "timing_peak_torso_to_peak_pelvis_rot_velo": "Timing between peak pelvis and torso rotation",
        "cog_velo_pkh": "Center of gravity velocity at peak knee height",
        "max_cog_velo_x": "Maximum center of gravity velocity in X direction",
        
        # Mechanics & Positioning
        "stride_length": "Distance from rear foot to lead foot at foot plant",
        "stride_angle": "Angle of stride direction",
        "arm_slot": "Arm angle at ball release",
        "torso_rotation_min": "Minimum torso rotation angle",
        
        # Joint Moments (Forces)
        "elbow_varus_moment": "Elbow varus stress",
        "shoulder_internal_rotation_moment": "Shoulder internal rotation stress",
        
        # Energy Transfer
        "shoulder_transfer_fp_br": "Shoulder energy transfer from foot plant to ball release",
        "shoulder_generation_fp_br": "Shoulder energy generation from foot plant to ball release", 
        "shoulder_absorption_fp_br": "Shoulder energy absorption from foot plant to ball release",
        "elbow_transfer_fp_br": "Elbow energy transfer from foot plant to ball release",
        "elbow_generation_fp_br": "Elbow energy generation from foot plant to ball release",
        "elbow_absorption_fp_br": "Elbow energy absorption from foot plant to ball release",
        "thorax_distal_transfer_fp_br": "Thorax distal energy transfer from foot plant to ball release"
    },
    
    "other_tables": {
        "users": ["user", "name", "dob", "traq"],
        "sessions": ["session", "user", "date", "level", "lab", "height_meters", "mass_kilograms"],
        "trials": ["session_trial", "session", "trial", "pitch_type", "handedness"],
        "drillscores": ["session", "traqid", "date", "pitch_speed_mph_score", "max_torso_rotational_velo_score"],
        "comp_scores_plus": ["session_trial", "arm_action", "block", "cog", "posture", "rot", "total"],
        "energetics": ["session_trial", "time", "shoulder_energy_transfer", "elbow_energy_transfer"],
        "force_plates": ["session_trial", "time", "rear_force_x", "rear_force_y", "rear_force_z", "lead_force_x", "lead_force_y", "lead_force_z"],
        "joint_angles": ["session_trial", "time", "elbow_angle_x", "shoulder_angle_x", "pelvis_angle_x"],
        "joint_forces": ["session_trial", "time", "elbow_force_x", "shoulder_upper_arm_force_x"],
        "joint_moments": ["session_trial", "time", "elbow_moment_x", "shoulder_thorax_moment_x"]
    }
}

# Complete Hitting Database Schema  
HITTING_COMPLETE_SCHEMA = {
    "database_name": "theia_hitting_db",
    "description": "Complete biomechanical analysis for baseball hitting",
    
    "poi_metrics": {
        # Performance Metrics
        "exit_velo_mph": "Ball exit velocity off bat",
        "blast_bat_speed_mph": "Bat speed from Blast sensor",
        "bat_speed_max": "Maximum bat speed during swing",
        "bat_speed_xy_max": "Maximum bat speed in horizontal plane",
        "bat_speed_contact": "Bat speed at contact",
        "attack_angle_contact": "Bat angle at contact",
        
        # Hand & Arm Speed
        "blast_hand_speed_max": "Maximum hand speed from Blast sensor",
        "hand_speed_max": "Maximum hand speed",
        "hand_speed_load": "Hand speed at load position",
        "hand_speed_fp": "Hand speed at foot plant", 
        "hand_speed_mhss": "Hand speed at maximum hand speed",
        "hand_speed_contact": "Hand speed at contact",
        
        # Rotational Velocities
        "peak_pelvis_ang_velo": "Peak pelvis angular velocity",
        "peak_torso_ang_velo": "Peak torso angular velocity", 
        "peak_upper_arm_ang_velo": "Peak upper arm angular velocity",
        "peak_hand_ang_velo": "Peak hand angular velocity",
        
        # Center of Gravity
        "cog_velo_x_fp": "Center of gravity velocity at foot plant",
        "cog_velo_x_max": "Maximum center of gravity velocity",
        
        # Bat Position & Orientation
        "sweet_spot_velo_x_contact": "Sweet spot velocity X at contact",
        "sweet_spot_velo_y_contact": "Sweet spot velocity Y at contact", 
        "sweet_spot_velo_z_contact": "Sweet spot velocity Z at contact",
        "bat_torso_angle_x_ds": "Bat-torso angle X at deep stride",
        "bat_torso_angle_y_ds": "Bat-torso angle Y at deep stride",
        "bat_torso_angle_z_ds": "Bat-torso angle Z at deep stride",
        
        # Pelvis Angles Throughout Swing
        "pelvis_angle_x_load": "Pelvis X angle at load",
        "pelvis_angle_x_fm": "Pelvis X angle at forward move",
        "pelvis_angle_x_fp": "Pelvis X angle at foot plant",
        "pelvis_angle_x_mhss": "Pelvis X angle at max hand speed",
        "pelvis_angle_x_contact": "Pelvis X angle at contact",
        "pelvis_angle_x_stride": "Pelvis X angle during stride",
        "pelvis_angle_x_swing": "Pelvis X angle during swing",
        
        "pelvis_angle_y_load": "Pelvis Y angle at load",
        "pelvis_angle_y_fm": "Pelvis Y angle at forward move", 
        "pelvis_angle_y_fp": "Pelvis Y angle at foot plant",
        "pelvis_angle_y_mhss": "Pelvis Y angle at max hand speed",
        "pelvis_angle_y_contact": "Pelvis Y angle at contact",
        "pelvis_angle_y_stride": "Pelvis Y angle during stride",
        "pelvis_angle_y_swing": "Pelvis Y angle during swing",
        
        "pelvis_angle_z_load": "Pelvis Z angle at load",
        "pelvis_angle_z_fm": "Pelvis Z angle at forward move",
        "pelvis_angle_z_fp": "Pelvis Z angle at foot plant", 
        "pelvis_angle_z_mhss": "Pelvis Z angle at max hand speed",
        "pelvis_angle_z_contact": "Pelvis Z angle at contact",
        "pelvis_angle_z_stride": "Pelvis Z angle during stride",
        "pelvis_angle_z_swing": "Pelvis Z angle during swing",
        
        # Torso Angles Throughout Swing
        "torso_angle_x_load": "Torso X angle at load",
        "torso_angle_x_fm": "Torso X angle at forward move",
        "torso_angle_x_fp": "Torso X angle at foot plant",
        "torso_angle_x_mhss": "Torso X angle at max hand speed",
        "torso_angle_x_contact": "Torso X angle at contact",
        "torso_angle_x_stride": "Torso X angle during stride",
        "torso_angle_x_swing": "Torso X angle during swing",
        
        "torso_angle_y_load": "Torso Y angle at load",
        "torso_angle_y_fm": "Torso Y angle at forward move",
        "torso_angle_y_fp": "Torso Y angle at foot plant",
        "torso_angle_y_mhss": "Torso Y angle at max hand speed", 
        "torso_angle_y_contact": "Torso Y angle at contact",
        "torso_angle_y_stride": "Torso Y angle during stride",
        "torso_angle_y_swing": "Torso Y angle during swing",
        
        "torso_angle_z_load": "Torso Z angle at load",
        "torso_angle_z_fm": "Torso Z angle at forward move",
        "torso_angle_z_fp": "Torso Z angle at foot plant",
        "torso_angle_z_mhss": "Torso Z angle at max hand speed",
        "torso_angle_z_contact": "Torso Z angle at contact",
        "torso_angle_z_stride": "Torso Z angle during stride", 
        "torso_angle_z_swing": "Torso Z angle during swing"
    },
    
    "other_tables": {
        "users": ["user", "name", "dob", "traq"],
        "sessions": ["session", "user", "date", "level", "lab", "height_meters", "mass_kilograms"],
        "trials": ["session_trial", "session", "trial", "handedness"],
        "blast_kvest": ["session_trial", "time", "bat_speed_mph_x", "attack_angle_x", "hand_speed_mag_x"],
        "comp_scores_plus": ["session_trial", "stride_rot", "stride_posture", "swing_posture", "swing_rot", "cog", "total"]
    }
}

def get_complete_schema_context() -> str:
    """Generate the most comprehensive schema context for LLM-based querying"""
    
    return f"""
# COMPLETE Baseball Biomechanics Database Schema

## Overview
You have access to the most comprehensive baseball biomechanics databases in existence:
- **theia_pitching_db**: Complete pitching mechanics with {len(PITCHING_COMPLETE_SCHEMA['poi_metrics'])} core metrics
- **theia_hitting_db**: Complete hitting mechanics with {len(HITTING_COMPLETE_SCHEMA['poi_metrics'])} core metrics

## Database Relationship Chain
**users** → **sessions** → **trials** → **poi** (core metrics)

## PITCHING METRICS (theia_pitching_db.poi)

### Performance & Velocity
- pitch_speed_mph: Ball velocity at release
- max_shoulder_internal_rotational_velo: Peak shoulder rotation speed  
- max_elbow_extension_velo: Peak elbow extension speed
- max_torso_rotational_velo: Peak torso rotation speed
- max_pelvis_rotational_velo: Peak pelvis rotation speed

### Mechanics & Positions
- stride_length: Distance from rear foot to lead foot
- arm_slot: Arm angle at ball release
- max_rotation_hip_shoulder_separation: Hip-shoulder separation
- max_elbow_flexion: Maximum elbow bend
- max_shoulder_external_rotation: Maximum shoulder external rotation

### Timing & Sequencing  
- timing_peak_torso_to_peak_pelvis_rot_velo: Kinematic sequencing timing
- lead_knee_extension_angular_velo_max: Lead knee extension speed
- cog_velo_pkh: Center of gravity velocity

### Joint Stress & Forces
- elbow_varus_moment: Elbow stress
- shoulder_internal_rotation_moment: Shoulder stress

## HITTING METRICS (theia_hitting_db.poi)

### Performance & Contact
- exit_velo_mph: Ball exit velocity off bat
- blast_bat_speed_mph: Bat speed at contact
- attack_angle_contact: Bat angle at contact
- blast_hand_speed_max: Maximum hand speed

### Rotational Power
- peak_pelvis_ang_velo: Peak pelvis rotation speed
- peak_torso_ang_velo: Peak torso rotation speed
- peak_upper_arm_ang_velo: Peak arm rotation speed

### Body Position Throughout Swing
Positions tracked at: load, forward_move, foot_plant, max_hand_speed, contact, stride, swing
- pelvis_angle_x/y/z_[position]: Pelvis orientation
- torso_angle_x/y/z_[position]: Torso orientation

## NATURAL LANGUAGE QUERY CAPABILITIES

Ask ANY question about baseball biomechanics:

**Player Analysis:**
- "Show me John's velocity progression over time"
- "How does Sarah's bat speed compare to team average?"
- "Find Mike's best throwing session"

**Comparative Analysis:**  
- "Compare shoulder rotation between pitchers and position players"
- "Which hitters have the most consistent attack angles?"
- "Show velocity differences between age groups"

**Mechanical Analysis:**
- "Find correlations between stride length and velocity"
- "Show players with improving hip-shoulder separation"
- "Analyze timing patterns in successful hitters"

**Population Studies:**
- "What's the average exit velocity by position?"
- "Show velocity distribution across all pitchers"
- "Find outliers in elbow stress measurements"

**Trend Analysis:**
- "Track velocity changes over the season"
- "Show improvement patterns after training"
- "Identify declining performance metrics"

## QUERY PATTERNS

The system automatically:
- Determines which database to use based on your question
- Joins the appropriate tables (users → sessions → trials → poi)
- Handles player name matching with partial searches
- Groups data by time periods for trends
- Calculates averages, maximums, and percentiles
- Formats results for easy interpretation

You don't need to know SQL - just ask your question in natural language!
"""

def get_all_pitching_metrics():
    """Get all available pitching metrics with descriptions"""
    return PITCHING_COMPLETE_SCHEMA['poi_metrics']

def get_all_hitting_metrics():
    """Get all available hitting metrics with descriptions"""
    return HITTING_COMPLETE_SCHEMA['poi_metrics']

def get_metric_by_name(metric_name: str, database: str = None):
    """Find a metric by name across databases"""
    results = []
    
    if database != "theia_hitting_db":
        for metric, desc in PITCHING_COMPLETE_SCHEMA['poi_metrics'].items():
            if metric_name.lower() in metric.lower() or metric_name.lower() in desc.lower():
                results.append({
                    "database": "theia_pitching_db",
                    "metric": metric,
                    "description": desc
                })
    
    if database != "theia_pitching_db":
        for metric, desc in HITTING_COMPLETE_SCHEMA['poi_metrics'].items():
            if metric_name.lower() in metric.lower() or metric_name.lower() in desc.lower():
                results.append({
                    "database": "theia_hitting_db", 
                    "metric": metric,
                    "description": desc
                })
    
    return results