import datetime
from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient
import os
import logging
import mongoDB as mdb
from dotenv import load_dotenv
load_dotenv()

# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("slack_bot_token"))
user_client = WebClient(token=os.environ.get("slack_user_token"))
logger = logging.getLogger(__name__)


def sendTextMessage(channel_id, text, file):

    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=channel_id,
            text=text,
            file=file,
            filename="image.png",
            # thread_ts="1687410571.722519"
        )
        logger.info(result)
        print("text msg ", result)
        return result

    except Exception as e:
        logger.error(f"Error posting message: {e}")

# Dispatch action


def send_farmer_query(channel_id, query_text, data):
    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=channel_id,
            text=query_text,
            blocks=data

        )
        logger.info(result)
        print("query text msg ", result)
        return result

    except Exception as e:
        logger.error(f"Error posting message: {e}")


# send_farmer_query("C05A8BJRK54", "query_text")


def sendForModeration(query_text, solution_text, agro_name):
    channel_id = "C05A8BJRK54"

    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=channel_id,
            text=solution_text,
            blocks=[
                # {
                #     "type": "header",
                #     "text": {
                #         "type": "plain_text",
                #         "text": "Solution",
                #         "emoji": True
                #     }
                # },
                {
                    "type": "section",
                    "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Query:*\n"+query_text
                            }
                    ]
                },
                {
                    "type": "section",
                    "fields": [

                        {
                            "type": "mrkdwn",
                            "text": "*Solution:*\n"+solution_text
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*by:*\n"+agro_name
                        }
                    ]
                },

                {
                    "type": "actions",
                    "elements": [
                            {
                                "type": "button",
                                "text": {
                                        "type": "plain_text",
                                        "emoji": True,
                                        "text": "Approve"
                                },
                                "style": "primary",
                                "value": "btn_approve",
                                "action_id": "btn_approve"
                            },
                        {
                                "type": "button",
                                "text": {
                                        "type": "plain_text",
                                        "emoji": True,
                                        "text": "Reject"
                                },
                                "style": "danger",
                                "value": "btn_reject",
                                "action_id": "btn_reject"
                            }
                    ]
                }
            ]

        )
        # /print(result)
        logger.info(result)

    except Exception as e:
        logger.error(f"Error posting message: {e}")
        print("Error posting message: {e}")


def get_user(userID):
    try:
        user_info = client.users_profile_get(user=userID)
        # print(user_info)
        return user_info

    except Exception as e:
        logger.error(f"Error posting message: {e}")
        print("Error get user profile: {e}")


def update_chat_message(channel_id, ts, update_text, data):
    result = client.chat_update(
        channel=channel_id,
        ts=ts,
        text=update_text,
        blocks=data


    )
    print(result)


def update_Approved_block(channel_id, ts, query, agro_name, solution_text, moderator_name, ):
    result = client.chat_update(
        channel=channel_id,
        ts=ts,

        blocks=[
            # {
            #     "type": "header",
            #     "text": {
            #         "type": "plain_text",
            #         "text": "New request",
            #         "emoji": True
            #     }
            # },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Query:*\n"+query
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*by:*\n"+agro_name
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Approved Solution:* "+solution_text
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Approved by:* "+moderator_name
                    }
                ]
            }
        ]

    )
    print(result)


def update_rejected_block(channel_id, ts, query, agro_name, solution_text, moderator_name, ):
    channel_id = "C05A8BJRK54"

    result = client.chat_update(
        channel=channel_id,
        ts=ts,

        blocks=[
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Query:*\n"+query
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Solution:*\n"+solution_text
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*by:*\n"+agro_name
                    }
                ]
            },
            {
                "dispatch_action": True,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "dispatch_action_config": {
                        "trigger_actions_on": [
                            "on_enter_pressed"
                        ]
                    },
                    "action_id": "moderated_comment"
                },
                "label": {
                    "type": "plain_text",
                            "text": "Comment",
                    "emoji": True
                }
            }
        ]


    )
    print(result)


def update_after_dm(channel_id, ts, query, agro_name, solution_text, comment):
    channel_id = "C05A8BJRK54"

    result = client.chat_update(
        channel=channel_id,
        ts=ts,

        blocks=[
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Query:*\n"+query
                    }
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Solution:*\n"+solution_text
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*by:*\n"+agro_name
                    }
                ]
            },
            {
                "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Comment:*\n"+comment
                            }
                        ]
            }
        ]


    )
    print(result)


def get_query_message(channel_id, ts):
    try:
        # Call the conversations.history method using the WebClient
        # The client passes the token you included in initialization
        result = client.conversations_history(
            channel=channel_id,
            inclusive=True,
            oldest=ts,
            limit=1
        )

        message = result["messages"][0]
        # Print message text
        print(message["text"])
        return message["text"]

    except SlackApiError as e:
        print(f"Error: {e}")


def dm_agronomist(agro_id, query_text, solution_text, comment, moderator_name):
    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=agro_id,
            text="",
            blocks=[
                {
                    "type": "section",
                    "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Query:*\n"+query_text
                            }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Solution:*\n"+solution_text
                            }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Comment:*\n"+comment
                            }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Comment by:*\n"+moderator_name
                            }
                    ]
                }
            ]

            # thread_ts="1687410571.722519"
        )
        logger.info(result)
        print("dm text msg ", result)
        return result

    except Exception as e:
        logger.error(f"Error posting message: {e}")


def dm_approved_sol(agro_id, query_text, solution_text, moderator_name):
    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=agro_id,
            text="",
            blocks=[
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Your solution has been approved!",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Query:*\n"+query_text
                            }
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Solution:*\n"+solution_text
                            }
                    ]
                },

                {
                    "type": "section",
                    "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "*Moderated by:*\n"+moderator_name
                            }
                    ]
                }
            ]

            # thread_ts="1687410571.722519"
        )
        logger.info(result)
        print("dm approve text msg ", result)
        return result

    except Exception as e:
        logger.error(f"Error posting message: {e}")


def convert_epoch_to_datetime(epoch):
    try:
        # Convert epoch to datetime
        dt = datetime.datetime.fromtimestamp(epoch)
        return dt
    except OSError as e:
        print("Error occurred during conversion:", e)


def convert_datetime_to_epoch(dt):
    try:
        # Convert datetime to epoch
        epoch = int(dt.timestamp())
        epoch_str = str(epoch) + "." + str(dt.microsecond)
        return epoch_str
    except OSError as e:
        print("Error occurred during conversion:", e)


def find_sol_timestamp(agro_name, text):
    retrieved_solutions = mdb.retrieve_agro_field(
        agro_name, "pending_solutions")

    result = next(
        (subarray for subarray in retrieved_solutions if text in subarray), None)
    print(result)
    return result


# Example usage
# epoch = 1687438739.320199  # Replace with your desired epoch timestamp
# datetime_obj = convert_epoch_to_datetime(epoch)
# print("Epoch 1 :", epoch)
# print("Datetime:", datetime_obj)

# # Example usage
# # Replace with your desired datetime
# datetime_obj = datetime.datetime(2023, 6, 22, 18, 28, 59, 320199)
# epoch = convert_datetime_to_epoch(datetime_obj)
# print("Datetime 2 :", datetime_obj)
# print("Epoch:", epoch)
