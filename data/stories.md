## travel with no message
* travel_none
  - travel_form
  - form{"name": "travel_form"}
  - form{"name": null}
* affirm
  - form{"name": null}
  - action_deactivate_form
  - utter_goodbye
* deny
  - action_deactivate_form  
  - form{"name": null}
## tavel with all_time
* travel_all_time
  - travel_form
  - form{"name":"travel_form"}
  - form{"name": null}
* affirm
  - form{"name": null}
  - action_deactivate_form
  - utter_goodbye
* deny
  - action_deactivate_form  
  - form{"name": null}
  - utter_deny_say

  
# story_travel_all_time_place_transport
* travel_all_time_place_transport
  - travel_form
  - form{"name":"travel_form"}
  - form{"name": null}
* affirm
  - form{"name": null}
  - action_deactivate_form
  - utter_goodbye
* deny
  - action_deactivate_form  
  - form{"name": null}
  
# story_travel_all_time_end_place  
* travel_all_time_end_place  
  - travel_form
  - form{"name":"travel_form"}
  - form{"name": null}
* affirm
  - form{"name": null}
  - action_deactivate_form
  - utter_goodbye
* deny
  - action_deactivate_form  
  - form{"name": null}
  - utter_goodbye
  
# story_travel_end_place
* travel_end_place
 - travel_form
  - form{"name":"travel_form"}
  - form{"name": null}
* affirm
  - form{"name": null}
  - action_deactivate_form
  - utter_goodbye
* deny
  - action_deactivate_form  
  - form{"name": null}
  - utter_goodbye

  
## story_greet
* greet
 - utter_greet
 
## story_address
* address
 - utter_address 
 
## story_time_entity
* time_entity
 - utter_time_entity

## story_user_idiom
* skills_user_idiom
 - user_action_user_idiom