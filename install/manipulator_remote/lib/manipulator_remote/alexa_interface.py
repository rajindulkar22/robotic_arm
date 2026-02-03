#!/usr/bin/env python3
from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from manipulator_msgs.action import ManipulatorTask
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize ROS2
rclpy.init()
node = Node("alexa_interface")
action_client = ActionClient(node, ManipulatorTask, "task_server")

# Start ROS2 spinning in a separate thread
threading.Thread(target=lambda: rclpy.spin(node), daemon=True).start()

app = Flask(__name__)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hi, How can I help you? You can say pick the pen, sleep, or wake up."
        
        logger.info("LaunchRequest received")
        
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Manipulator Control", speech_text)).set_should_end_session(False)
        
        # Send goal to initialize robot
        try:
            goal = ManipulatorTask.Goal()
            goal.task_number = 0
            action_client.send_goal_async(goal)
            logger.info("Sent initialization goal (task 0)")
        except Exception as e:
            logger.error(f"Error sending goal: {e}")
        
        return handler_input.response_builder.response


class PickIntentHandler(AbstractRequestHandler):
    """Handler for Pick Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PickIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Okay, I am picking up the object now."
        
        logger.info("PickIntent received")
        
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Pick Object", speech_text)).set_should_end_session(True)
        
        # Send pick goal
        try:
            goal = ManipulatorTask.Goal()
            goal.task_number = 1
            action_client.send_goal_async(goal)
            logger.info("Sent pick goal (task 1)")
        except Exception as e:
            logger.error(f"Error sending goal: {e}")
        
        return handler_input.response_builder.response


class SleepIntentHandler(AbstractRequestHandler):
    """Handler for Sleep Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SleepIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Okay, I am going to sleep now. Goodnight!"
        
        logger.info("SleepIntent received")
        
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Sleep Mode", speech_text)).set_should_end_session(True)
        
        # Send sleep goal
        try:
            goal = ManipulatorTask.Goal()
            goal.task_number = 2
            action_client.send_goal_async(goal)
            logger.info("Sent sleep goal (task 2)")
        except Exception as e:
            logger.error(f"Error sending goal: {e}")
        
        return handler_input.response_builder.response


class WakeIntentHandler(AbstractRequestHandler):
    """Handler for Wake Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("WakeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Okay, I am awake and ready to work!"
        
        logger.info("WakeIntent received")
        
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Wake Mode", speech_text)).set_should_end_session(True)
        
        # Send wake goal
        try:
            goal = ManipulatorTask.Goal()
            goal.task_number = 3
            action_client.send_goal_async(goal)
            logger.info("Sent wake goal (task 3)")
        except Exception as e:
            logger.error(f"Error sending goal: {e}")
        
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say pick the pen to pick up an object, sleep to turn off the robot, or wake up to activate the robot. What would you like to do?"
        
        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Help", speech_text))
        
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Handler for Cancel and Stop Intents."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye! See you next time."
        
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Goodbye", speech_text))
        
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("Session ended")
        return handler_input.response_builder.response


class AllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(f"Exception encountered: {exception}", exc_info=True)
        
        speech = "Sorry, I didn't understand that. Could you please repeat?"
        handler_input.response_builder.speak(speech).ask(speech)
        
        return handler_input.response_builder.response


# Build the skill
skill_builder = SkillBuilder()

# Add request handlers
skill_builder.add_request_handler(LaunchRequestHandler())
skill_builder.add_request_handler(PickIntentHandler())
skill_builder.add_request_handler(SleepIntentHandler())
skill_builder.add_request_handler(WakeIntentHandler())
skill_builder.add_request_handler(HelpIntentHandler())
skill_builder.add_request_handler(CancelOrStopIntentHandler())
skill_builder.add_request_handler(SessionEndedRequestHandler())

# Add exception handler
skill_builder.add_exception_handler(AllExceptionHandler())

# Create skill adapter
skill_adapter = SkillAdapter(
    skill=skill_builder.create(), 
    skill_id="amzn1.ask.skill.38eaeb24-1bc4-4480-a0e6-5c5900164070", 
    app=app
)

# Register the skill adapter with Flask (this handles routing automatically)
skill_adapter.register(app=app, route="/")


if __name__ == "__main__":
    # Use port 5001 to avoid conflicts
    port = 5001
    logger.info(f"Starting Flask app on port {port}")
    logger.info("Make sure to update your ngrok tunnel and Alexa endpoint!")
    app.run(host='0.0.0.0', port=port, debug=False)