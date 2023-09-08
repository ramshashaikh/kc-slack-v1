import requests
import slack_methods as sm
from slack_bolt import App
import os
import mongoDB as mdb
from dotenv import load_dotenv
load_dotenv()


# Initializes your app with your bot token and signing secret
app = App(
    token=os.getenv("slack_bot_token"),
    signing_secret=os.getenv("signing_secret")
)


def post_message_to_slack():

    user_id = mdb.retrieve_field("918779171731", "userID")
    if user_id != "No document found.":

        query_text = mdb.retrieve_field("918779171731", "query")
        image_data = mdb.retrieve_field("918779171731", "cloudinary_url")
        print("image_data ", image_data)
        image_array = []
        for i in image_data:
            # print("i ", i)
            image_array.append(
                {"type": "image", "image_url": i, "alt_text": "image_"+i})

        image_array.insert(0, {
            "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Query:*\n"+query_text
                        }
                    ]},
        )

        response = sm.send_farmer_query("C05A8BH2C22", query_text, image_array)

        # response = sm.sendTextMessage("C05A8BH2C22", query_text)
        # TODO: Add query id mechanism
        ts = response.get('ts')
        print(ts)

        mdb.update_field_set("918779171731", "posted_ts", ts)
        mdb.update_field_set("918779171731", "status", "Pending")

        mdb.create_query_record("KC_01", "918779171731", query_text, ts)


# post_message_to_slack()

url = 'https://files.slack.com/files-pri/T05A8BH0VJA-F05FNEM023B/dall__e_2023-04-13_07.59.58_-_charts_and_graphs_showing_market_trends__a_magnifying_glass_examining_data_points.png'
token = 'xoxb-5348391029622-5367699389473-dmFl6x1J3B9MHJkoO1sB8irU'
r = requests.get(url, headers={'Authorization': 'Bearer %s' % token})
print(r)
sm.sendTextMessage("C05A8BH2C22", "This is a test message",
                   "https://files.slack.com/files-pri/T05A8BH0VJA-F05FNEM023B/dall__e_2023-04-13_07.59.58_-_charts_and_graphs_showing_market_trends__a_magnifying_glass_examining_data_points.png")
# NOTE: in response as a thread message, thread_ts is the parent ts.


@app.message("")
def message_hello(message, say):
    print("message ", message)
    # From message body
    solution_text = message.get('blocks')[0].get(
        'elements')[0].get('elements')[0].get('text')
    parent_ts = message.get('thread_ts')
    current_ts = message.get('ts')

    # Find Agronomist name
    agro_id = message.get('user')
    user_info = sm.get_user(agro_id)
    agro_name = user_info.get('profile').get('real_name')

    # Find main query text, and use thatto find query_id
    query_text = sm.get_query_message("C05A8BH2C22", parent_ts)
    query_id = mdb.retrieve_query_field(query_text, "query_id")
    print("query_id ", query_id)

    # print("solution_text ", message, query_text,
    #       agro_name, parent_ts, current_ts)

    # [query_id, query_text,solution_text, current_ts]
    print("Updating pending solutions")
    mdb.update_push_agro(agro_id, "pending_solutions", {
                         "query_id": query_id,
                         "query_text": query_text,
                         "solution_text": solution_text,
                         "current_ts": current_ts})

    # agro_id, solution_text, current_ts
    mdb.update_push_query(query_id, "pending_solutions", {
                          "agro_id": agro_id, "solution_text": solution_text, "current_ts": current_ts})

    sm.sendForModeration(query_text, solution_text, agro_name)


@app.action("btn_approve")
def handle_some_action(ack, body, logger):
    ack()
    logger.info(body)
    # print("Approve ", body)
    # print("Approve message ", body)

    # Message body
    solution_text = body.get('message').get('text')
    action_ts = body.get('actions')[0].get('action_ts')
    print("action_ts ", action_ts)

    # Get agronomist name
    by_text = body.get(
        'message').get('blocks')[1].get('fields')[1].get('text')
    agro_name = by_text.split("\n")[1]
    agro_id = mdb.retrieve_agro_field(agro_name, "agro_id")

    query_text = body.get(
        'message').get('blocks')[0].get('fields')[0].get('text')
    query_text = query_text.split("\n")[1]

    print("Approve message ", agro_name, query_text)

    # Get query text

    query_id = mdb.retrieve_query_field(query_text, "query_id")
    query_posted_ts = mdb.retrieve_query_field(query_text, "posted_ts")

    # solution_ts = sm.find_sol_timestamp(agro_name, solution_text)
    # print("solution_ts ", solution_ts, query_text)

    # * Update main thread query message
    query_by = mdb.retrieve_query_field(query_text, "query_by")
    image_data = mdb.retrieve_field(query_by, "cloudinary_url")
    # print("image_data ", image_data)
    image_array = []
    for i in image_data:

        image_array.append(
            {"type": "image", "image_url": i, "alt_text": "image_"+i})

    image_array.insert(0,
                       {
                           "type": "header",
                           "text": {
                               "type": "plain_text",
                               "text": "Approved",
                               "emoji": True
                           }
                       })
    image_array.insert(1, {
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": "*Type:*\n "+query_text
            }
        ]
    })
    # print("image_array ", image_array)
    sm.update_chat_message("C05A8BH2C22", query_posted_ts,
                           query_text, data=image_array)

    # sm.update_chat_message(
    #     "C05A8BH2C22", query_posted_ts, "[Approved] "+query_text+"\n"+solution_text)

    current_ts = body.get('container').get('message_ts')

    moderator_name = body.get("user").get("name")
    print("current_ts ", current_ts, moderator_name)

    sm.update_Approved_block(
        "C05A8BJRK54", current_ts, query_text, agro_name, solution_text, moderator_name)

    dm_approve = sm.dm_approved_sol(
        agro_id, query_text, solution_text, moderator_name)

    # * Updating query table - remove from pending_solutions, add to approved_solutions
    # removing from pending_solutions
    mdb.update_pull_query(query_id, "pending_solutions", solution_text)
    # adding to approved_solutions
    mdb.update_set_queries(query_id, solution_text,
                           agro_name, moderator_name, action_ts)

    # * Update agronomist table - remove from pending_solutions, add to approved_solutions
    # [query_id, query_text, solution_text, moderator_name, action_ts]
    print("Approved - ", agro_id, solution_text)
    mdb.update_pull_agro(agro_id, "pending_solutions", solution_text)
    mdb.update_push_agro(agro_id, "approved_solutions", {"query_id": query_id,
                                                         "query_text": query_text,
                                                         "solution_text": solution_text,
                                                         "moderator_name": moderator_name,
                                                         "action_ts": action_ts,
                                                         })

    # TODO: change user status field

# print(sm.get_user("U05DC8WAU31")
#       )


@app.action("btn_reject")
def handle_some_action(ack, body, logger):
    ack()
    logger.info(body)
    print("Reject ", body)

    current_ts = body.get('container').get('message_ts')

    query_text = body.get(
        'message').get('blocks')[0].get('fields')[0].get('text')
    query_text = query_text.split("\n")[1]

    solution_text = body.get('message').get('text')
    action_ts = body.get('actions')[0].get('action_ts')
    print("action_ts ", action_ts)

    # Get agronomist name
    by_text = body.get(
        'message').get('blocks')[1].get('fields')[1].get('text')
    agro_name = by_text.split("\n")[1]
    agro_id = mdb.retrieve_agro_field(agro_name, "agro_id")
    moderator_name = body.get("user").get("name")

    sm.update_rejected_block("C05A8BJRK54", current_ts,
                             query_text, agro_name, solution_text, moderator_name)
    print("Reject message ", action_ts == current_ts)
    # TODO: Update query table - remove from pending_solutions, add to rejected_solutions
    # query_id = mdb.retrieve_query_field(query_text, "query_id")
    # # removing from pending_solutions
    # mdb.update_pull_query(query_id, "pending_solutions", solution_text)
    # # adding to approved_solutions
    # mdb.update_push_query(query_id, "rejected_solutions", [
    #                       agro_id, solution_text, moderator_name, action_ts])

    # # * Update agronomist table - remove from pending_solutions, add to rejected_solutions
    # mdb.update_pull_agro(agro_id, "pending_solutions", solution_text)
    # mdb.update_push_agro(agro_id, "rejected_solutions", [
    #                      query_id, query_text, solution_text, moderator_name, action_ts])


@app.action("moderated_comment")
def handle_some_action(ack, body, logger):
    ack()
    logger.info(body)

    # print(body)
    block_id = body.get('actions')[0].get('block_id')
    comment = body.get('actions')[0].get('value')
    action_ts = body.get('actions')[0].get('action_ts')

    current_ts = body.get('container').get('message_ts')
    print("block_id ", block_id, comment)
    # comment = body.get('state').get(
    #     'values').get('O/kl').get("moderated_comment").get('value')

    # print("Moderated comment ", comment)

    by_text = body.get(
        'message').get('blocks')[1].get('fields')[1].get('text')
    agro_name = by_text.split("\n")[1]
    agro_id = mdb.retrieve_agro_field(agro_name, "agro_id")

    query_text = body.get(
        'message').get('blocks')[0].get('fields')[0].get('text')
    query_text = query_text.split("\n")[1]

    solution_text = body.get(
        'message').get('blocks')[1].get('fields')[0].get('text')
    solution_text = solution_text.split("\n")[1]

    moderator_name = body.get("user").get("name")
    print("agro_name in moderated comment ", agro_name,
          agro_id, query_text, solution_text, moderator_name)

    dm_status = sm.dm_agronomist(
        agro_id, query_text, solution_text, comment, moderator_name)

    if dm_status.get('ok'):
        print("DM sent successfully")
        sm.update_after_dm("C05A8BJRK54", current_ts,
                           query_text, agro_name, solution_text, comment)

        query_id = mdb.retrieve_query_field(query_text, "query_id")
        # removing from pending_solutions
        mdb.update_pull_query(query_id, "pending_solutions", solution_text)
        # adding to approved_solutions - [agro_id, solution_text, moderator_name, action_ts]
        mdb.update_push_query(query_id, "rejected_solutions", {"agro_id": agro_id,
                                                               "solution_text": solution_text,
                                                               "moderator_name": moderator_name,
                                                               "comment_by_moderator": comment,
                                                               "action_ts": action_ts,
                                                               })

        # * Update agronomist table - remove from pending_solutions, add to rejected_solutions
        mdb.update_pull_agro(agro_id, "pending_solutions", solution_text)
        mdb.update_push_agro(agro_id, "rejected_solutions", {"query_id": query_id,
                                                             "query_text": query_text,
                                                             "solution_text": solution_text,
                                                             "moderator_name": moderator_name,
                                                             "comment_by_moderator": comment,
                                                             "action_ts": action_ts,
                                                             })

#


@app.event("file_shared")
def handle_file_events(body, logger):
    print("file_shared ", body)


# app.event("file_created")(handle_file_events)


@app.event("file_public")
def handle_file_events(body, logger):
    print("file_public ", body)


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)
    print("message ", body)


# mdb.update_push("918779171731", "Solution", [
#                 "This is a test message", "asss", "sss"])

# sm.find_sol_timestamp("918779171731", "s2")
# sm.sendTextMessage("C05A8BH2C22", "This is a test message")
# sm.update_chat_message(
#     "C05A8BH2C22", "1687438739.320199", "[]]")


# @app.action("plain_text_input-action")
# def handle_some_action(ack, body, logger):
#     ack()
#     print(body)
#     logger.info(body)
# say(f"Hey there <@{message['user']}>!")
# Start your app
if __name__ == "__main__":
    app.start(port=int(os.getenv("PORT", 3000)))
