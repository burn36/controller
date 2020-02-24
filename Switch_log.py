# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, HANDSHAKE_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.topology import event
import sys
import logging.handlers
import logging
from logging.handlers import RotatingFileHandler
from ryu.topology import switches,event
import ryu.utils as utils
from ryu.ofproto import ofproto_parser

class switchLog(app_manager.RyuApp):

    _CONTEXTS = {'switches': switches.Switches}
    EVENTS = [event.EventSwitchEnter, event.EventSwitchLeave,
               event.EventSwitchReconnected,
               event.EventPortAdd, event.EventPortDelete,
               event.EventPortModify,
               event.EventLinkAdd, event.EventLinkDelete,
               event.EventHostAdd,event.EventHostMove]

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        pass

    def __init__(self, *args, **kwargs):
        super(switchLog, self).__init__(*args, **kwargs)
        self.name = 'switchLog'

        self.switches = kwargs['switches']
        self.switches._EVENTS=self.EVENTS

        self.sending_echo_request_interval = 0.05
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s %(message)s',"%Y-%m-%d %H:%M:%S")

        # add formatter to ch
        ch.setFormatter(formatter)
        logFile = self.name+'.log'
        my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=0, encoding=None, delay=0)
        my_handler.setFormatter(formatter)
        # add ch to logger
        self.logger.addHandler(ch)

        # logname=self.name + '.log'
        # handler=logging.handlers.WatchedFileHandler(logname)
        # handler.setFormatter(formatter)
        # self.logger.addHandler(handler)

        self.logger.addHandler(my_handler)
    
   
    @set_ev_cls(ofp_event.EventOFPErrorMsg,[HANDSHAKE_DISPATCHER, CONFIG_DISPATCHER, MAIN_DISPATCHER])
    def error_msg_handler(self, ev):
        msg = ev.msg
        ofp = msg.datapath.ofproto
        dpid = msg.datapath.id

        self.logger.info("%s %s %s %s",dpid ,
            ofp.ofp_msg_type_to_str(msg.msg_type),
            ofp.ofp_error_type_to_str(msg.type),
            ofp.ofp_error_code_to_str(msg.type, msg.code))
        if len(msg.data) >= ofp.OFP_HEADER_SIZE:
            (version, msg_type, msg_len, xid) = ofproto_parser.header(msg.data)
            self.logger.info(
                "%s %s",dpid,
                ofp.ofp_msg_type_to_str(msg_type))
        else:
            self.logger.warning(
                "The data field sent from the switch is too short: "
                "len(msg.data) < OFP_HEADER_SIZE\n"
                "The OpenFlow Spec says that the data field should contain "
                "at least 64 bytes of the failed request.\n"
                "Please check the settings or implementation of your switch.")

    @set_ev_cls(event.EventPortAdd)
    def EventPortAdd(self, event):
        self.logger.info('EventPortAdd %s',event)  

    @set_ev_cls(event.EventPortDelete)
    def EventPortDelete(self, event):
        self.logger.info('EventPortDelete %s',event)  

    @set_ev_cls(event.EventPortModify)
    def EventPortModify(self, event):
        self.logger.info('EventPortModify %s',event)  

    @set_ev_cls(event.EventSwitchReconnected)
    def EventSwitchReconnected(self, event):
        self.logger.info('EventSwitchReconnected %s',event)  

    @set_ev_cls(event.EventSwitchEnter)
    def EventSwitchEnter(self, event):
        self.logger.info('EventSwitchEnter %s',event)  
        
    @set_ev_cls(event.EventSwitchLeave)
    def EventSwitchLeave(self, event):
        self.logger.info('EventSwitchLeave %s',event)  

    @set_ev_cls(event.EventHostMove)
    def EventHostMove(self, event):
        self.logger.info('EventHostMove %s',event)

    @set_ev_cls(event.EventHostAdd)
    def EventHostAdd(self, event):
        self.logger.info('EventHostAdd %s',event) 

    # Event laporan link topo add
    @set_ev_cls(event.EventLinkAdd)
    def EventLinkAdd(self, event):
        self.logger.info('topo discovery received %s',event)
       

    # Event laporan link topo delete
    @set_ev_cls(event.EventLinkDelete)
    def del_link(self, event):
        self.logger.info('link discovery timeout %s',event)

   