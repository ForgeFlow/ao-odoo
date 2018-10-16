=====================
Mail Activity Purpose
=====================

This module allows to record the purpose of the activity in a
categorized manner, in a dropdown field.

Configuration
=============

Go to *Settings > Technical > Email > Activity Purposes* and define the
purposes indicators. You can assign a progress indicator to several activity
types if you want the indicator to be specific to one or more types.

Usage
=====

Complete the purpose when creating or editing an activity.


Known issues / Roadmap
======================

* The button 'Mark done' that appears for each activity in the chatter
  is not available.

* It is not possible to schedule a next activity based on a given activity.

* In v9 a hook is needed in the method 'send_mail' of the transient
  model 'mail.compose.message'. Otherwise the completion of an activity
  will be notified to external partners. In v10 this feature exists out of
  of the box in Odoo.
