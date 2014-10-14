import rospy
import smach
import smach_ros
import actionlib
from mission_smach.states import get_next_point
from mission_smach.states import generate_waypoints
from position_action_server import *
from position_action_server.msg import *
from geometry_msgs.msg._PoseStamped import PoseStamped

def build():
    behaviour = smach.StateMachine(outcomes=['success','preempted','aborted'],output_keys=['next_x','next_y'])
    # Next go to point
    behaviour.userdata.next_x = 0.0
    behaviour.userdata.next_y = 0.0
    
    with behaviour :   
        smach.StateMachine.add('GENERATE_WAYPOINTS', generate_waypoints.generate(), 
                               transitions={'succeeded':'GET_NEXT'})     
        smach.StateMachine.add('GET_NEXT', get_next_point.getNextPosition(), 
                               transitions={'succeeded':'GO_TO_POINT', 'done':'success'})
        smach.StateMachine.add('GO_TO_POINT', 
                               smach_ros.SimpleActionState('/fmExecutors/position_planner',positionAction, goal_slots=['x','y']),
                               transitions={'succeeded':'GET_NEXT','preempted':'preempted','aborted':'aborted'},
                               remapping={'x':'next_x','y':'next_y'})   
      
    return behaviour
