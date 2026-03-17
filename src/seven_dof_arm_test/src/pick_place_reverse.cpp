#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>

using namespace std;

int main(int argc, char **argv) {

	ros::init(argc, argv, "seven_dof_arm_planner");
	ros::NodeHandle node_handle;
	ros::AsyncSpinner spinner(1);
	spinner.start();

	moveit::planning_interface::MoveGroupInterface group("arm");
	moveit::planning_interface::PlanningSceneInterface planning_scene_interface;

	sleep(2);

	moveit::planning_interface::PlanningSceneInterface current_scene;
	geometry_msgs::Pose pose;

	// 물체 생성 (y=-0.1 왼쪽에서 시작)
	shape_msgs::SolidPrimitive primitive;
	primitive.type = primitive.BOX;
	primitive.dimensions.resize(3);
	primitive.dimensions[0] = 0.03;
	primitive.dimensions[1] = 0.03;
	primitive.dimensions[2] = 0.08;

	moveit_msgs::CollisionObject grasping_object;
	grasping_object.id = "grasping_object";
	pose.orientation.w = 1.0;
	pose.position.x = 0.41;
	pose.position.y = -0.1;
	pose.position.z = 0.35;
	grasping_object.primitives.push_back(primitive);
	grasping_object.primitive_poses.push_back(pose);
	grasping_object.operation = grasping_object.ADD;
	grasping_object.header.frame_id = "base_link";

	// 테이블 생성
	primitive.dimensions.resize(3);
	primitive.dimensions[0] = 0.3;
	primitive.dimensions[1] = 0.5;
	primitive.dimensions[2] = 0.32;
	moveit_msgs::CollisionObject grasping_table;
	grasping_table.id = "grasping_table";
	pose.position.x = 0.46;
	pose.position.y = 0.0;
	pose.position.z = 0.15;
	grasping_table.primitives.push_back(primitive);
	grasping_table.primitive_poses.push_back(pose);
	grasping_table.operation = grasping_object.ADD;
	grasping_table.header.frame_id = "base_link";

	std::vector<moveit_msgs::CollisionObject> collision_objects;
	collision_objects.push_back(grasping_object);
	collision_objects.push_back(grasping_table);
	current_scene.addCollisionObjects(collision_objects);

	moveit::planning_interface::MoveGroupInterface::Plan my_plan;
	const robot_state::JointModelGroup *joint_model_group =
		group.getCurrentState()->getJointModelGroup("arm");

	geometry_msgs::Pose target_pose;
	target_pose.orientation.x = 0;
	target_pose.orientation.y = 0;
	target_pose.orientation.z = 0;
	target_pose.orientation.w = 1;

	// [1] 접근
	target_pose.position.x = 0.28;
	target_pose.position.y = -0.1;
	target_pose.position.z = 0.35;
	group.setPoseTarget(target_pose);
	group.move();
	sleep(1);
	cout << "First motion done!" << endl;

	// [2] 파지
	target_pose.position.x = 0.34;
	target_pose.position.y = -0.1;
	target_pose.position.z = 0.35;
	group.setPoseTarget(target_pose);
	group.move();
	sleep(1);
	cout << "Grasped!" << endl;

	// [3] 물체 붙이기
	moveit_msgs::AttachedCollisionObject att_coll_object;
	att_coll_object.object.id = "grasping_object";
	att_coll_object.link_name = "gripper_finger_link1";
	att_coll_object.object.operation = att_coll_object.object.ADD;
	planning_scene_interface.applyAttachedCollisionObject(att_coll_object);
	sleep(2);

	// [4] 살짝 들어올리기
	target_pose.position.x = 0.34;
	target_pose.position.y = -0.1;
	target_pose.position.z = 0.42;
	group.setPoseTarget(target_pose);
	group.move();
	sleep(1);
	cout << "Lifted!" << endl;

	// [5] 반대편으로 이동 (y=+0.1)
	target_pose.position.x = 0.28;
	target_pose.position.y = 0.1;
	target_pose.position.z = 0.42;
	group.setPoseTarget(target_pose);
	group.move();
	sleep(1);
	cout << "Moved to opposite!" << endl;

	// [6] 내려놓기
	target_pose.position.x = 0.28;
	target_pose.position.y = 0.1;
	target_pose.position.z = 0.35;
	group.setPoseTarget(target_pose);
	group.move();
	sleep(1);
	cout << "Placed!" << endl;

	// [7] 물체 분리
	att_coll_object.object.operation = att_coll_object.object.REMOVE;
	att_coll_object.link_name = "gripper_finger_link1";
	att_coll_object.object.id = "grasping_object";
	planning_scene_interface.applyAttachedCollisionObject(att_coll_object);
	sleep(1);

	// [8] 팔 뒤로 빼기
	target_pose.position.x = 0.20;
	target_pose.position.y = 0.1;
	target_pose.position.z = 0.35;
	group.setPoseTarget(target_pose);
	group.move();

	cout << "Done! 물체를 y=+0.1 반대편에 놓았습니다." << endl;

	ros::shutdown();
}