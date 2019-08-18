# -*- coding: utf-8 -*-
import json
import logging
from typing import Dict, Text, Any, List, Union, Optional

import requests
from rasa_sdk import Tracker
from rasa_sdk.events import Restarted, AllSlotsReset
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT

import YytUtils

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def extract_travel_all_time_slot(dispatcher: CollectingDispatcher, tracker: Tracker):
    print("指明开始时间和结束时间")
    current_user_msg = tracker.latest_message.get('text')
    print("用户说", current_user_msg)
    # 判断意图 看看是不是目标意图，是目标意图，是目标意图判断时间的词槽有没有数据
    # （没有数据判断用户输入是不是包含了起始和结束的话术，目前这个可以通过语料的入选类型来严格控制进入意图的准入条件）
    entities = tracker.latest_message['entities']
    start_time = ''
    end_time = ''
    slots_set = []
    if len(entities) == 2:
        for tmp in entities:
            if tmp.get("entity") == "start_time":
                logger.debug("start_time=", tmp.get("value"))
                start_time = tmp.get("value");
            if tmp.get("entity") == "end_time":
                logger.debug("end_time=", tmp.get("value"))
                end_time = tmp.get("value")
    else:
        date = YytUtils.get_date(current_user_msg)
        try:
            start_time = date[0]
            end_time = date[1]
        except IndexError as  e:
            logger.error(e)
    tracker.slots["start_time"] = start_time
    tracker.slots["end_time"] = end_time
    slots_set.append(SlotSet("start_time", start_time))
    slots_set.append(SlotSet("end_time", end_time))
    return slots_set
    # 分词找出结束和起始时间


class TravelForm(FormAction):
    # 已知开始时间和结束时间
    TRAVEL_ALL_TIME = "travel_all_time"

    def name(self):
        return "travel_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        print("required_slots:>", tracker.latest_message['intent'].get('name'))
        required_tmp_slots = ["start_time", "end_time", "start_place", "end_place", "transport"]
        required_slots = []
        start_time = tracker.get_slot("start_time")
        end_time = tracker.get_slot("end_time")
        start_place = tracker.get_slot("start_place")
        end_place = tracker.get_slot("end_place")
        transport = tracker.get_slot("transport")
        print(start_time, end_time, start_place, end_place, transport)
        if start_time is None:
            required_slots.append("start_time")
        if end_time is None:
            required_slots.append("end_time")
        if start_place is None:
            required_slots.append("start_place")
        if end_place is None:
            required_slots.append("end_place")
        if transport is None:
            required_slots.append("transport")
        return required_slots

    def submit(self, dispatcher, tracker, domain):
        print("结束提交", domain.values())
        if tracker.get_slot("start_time") and tracker.get_slot("end_time") and tracker.get_slot("start_place") \
                and tracker.get_slot("end_place") and tracker.get_slot("transport") is not None:
            info = '信息如下:\n出发时间\t: {0}\n返回时间\t: {1}\n出发地点\t: {2}\n目的地点\t : {3}\n交通工具\t: {4}\n 确定请回答是否则不是' \
                .format(tracker.get_slot("start_time"), tracker.get_slot("end_time"),
                        tracker.get_slot("start_place"), tracker.get_slot("end_place"),
                        tracker.get_slot("transport")
                        )
            print(info)
            # buttons = []
            # # 确定按钮
            # buttons.append(
            #     {"title": "{}".format("确定"), "payload": "/affirm"}
            # )
            # # 取消按钮
            # buttons.append({"title": "{}".format("取消"), "payload": "/deny"}
            #                )
            dispatcher.utter_message(info)
        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "start_time": self.from_text(),
            "end_time": self.from_text(),
            "start_place": self.from_text(),
            "end_place": self.from_text(),
            "transport": self.from_text(),
        }

    def request_next_slot(
            self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain,  # type: Dict[Text, Any]
    ):
        # type: (...) -> Optional[List[Dict]]
        """Request the next slot and utter template if needed,
            else return None"""

        print("Intent:>", tracker.latest_message['intent'].get('name'))
        print("latest_latest_message>>", tracker.latest_message)
        print("latest_latest_action_name>>", tracker.latest_action_name)
        print("user:>", tracker.latest_message.get('text'))
        print(tracker.get_slot("end_time"), tracker.get_slot("start_time"))
        slots_set = []
        if tracker.latest_message['intent'].get('name') == self.TRAVEL_ALL_TIME:
            print("send--id", tracker.sender_id)
            slots_set = extract_travel_all_time_slot(dispatcher, tracker)
        if tracker.latest_message['intent'].get('name') == 'restart':
            print("last_msg", tracker.latest_message['intent'])
            return [Restarted(), AllSlotsReset()]
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                logger.debug("Request next slot '{}'".format(slot))
                print("Request next slot '{}'".format(slot))
                dispatcher.utter_template(
                    "utter_ask_{}".format(slot),
                    tracker,
                    silent_fail=False,
                    **tracker.slots
                )
                slots_set.append(SlotSet(REQUESTED_SLOT, slot))
                return slots_set
        return None

    # 用来抽取 指明了开始时间和结束时间的

    def extract_requested_slot(
            self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain,  # type: Dict[Text, Any]
    ):
        # type: (...) -> Dict[Text: Any]
        """Extract the value of requested slot from a user input
            else return None
        """
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        logger.debug("Trying to extract requested slot '{}' ...".format(slot_to_fill))

        # get mapping for requested slot
        requested_slot_mappings = self.get_mappings_for_slot(slot_to_fill)
        if tracker.latest_message['intent'].get('name') == self.TRAVEL_ALL_TIME:
            extract_travel_all_time_slot(dispatcher, tracker)
        for requested_slot_mapping in requested_slot_mappings:
            logger.debug("Got mapping '{}'".format(requested_slot_mapping))
            if self.intent_is_desired(requested_slot_mapping, tracker):
                mapping_type = requested_slot_mapping["type"]
                if mapping_type == "from_entity":
                    value = self.get_entity_value(
                        requested_slot_mapping.get("entity"), tracker
                    )
                elif mapping_type == "from_intent":
                    value = requested_slot_mapping.get("value")
                elif mapping_type == "from_trigger_intent":
                    # from_trigger_intent is only used on form activation
                    continue
                elif mapping_type == "from_text":
                    value = tracker.latest_message.get("text")
                else:
                    raise ValueError("Provided slot mapping type is not supported")

                if value is not None:
                    logger.debug(
                        "Successfully extracted '{}' "
                        "for requested slot '{}'"
                        "".format(value, slot_to_fill)
                    )
                    print("填充了:", slot_to_fill)
                    return {slot_to_fill: value}
        print("text__________", tracker.latest_message.get("text"))
        logger.debug("Failed to extract requested slot '{}'".format(slot_to_fill))
        return {}


class BaiDuAction(FormAction):
    @staticmethod
    def required_slots(tracker):
        return []

    def submit(self, dispatcher, tracker, domain):
        # slot = tracker.get_slot("user_idiom")
        # slot = tracker.get_slot("user_keyword")
        msg = tracker.latest_message.get("text")
        bot = sendMsgToChatBot(msg)
        dispatcher.utter_message(bot)
        return []

    def name(self):
        return "user_baidu_search"


class UserIdiomAction(FormAction):
    def name(self):
        return "user_action_user_idiom"

    @staticmethod
    def required_slots(tracker):
        print("需要的槽位")
        return ["user_idiom"]

    def submit(self, dispatcher, tracker, domain):
        idiom = tracker.get_slot("user_idiom")
        print(idiom)
        intent_ = tracker.latest_message['intent']
        print("intent", intent_)
        dispatcher.utter_message("{}的意思是.......，哈哈哈，其实我要不知道".format(idiom))
        return []


def sendMsgToChatBot(txt):
    print(txt)
    response = requests.post(
        "http://10.188.181.72:9999/message",
        data={"msg": txt}
    )
    print(response.text)
    resultMsg = response.text
    try:
        res = json.dumps(response.text)
        resultMsg = res['text']
    except  BaseException as  e:
        print(e)
    return resultMsg
