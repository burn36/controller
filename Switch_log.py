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
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.topology import event
import logging
import sys
import logging.handlers
from ryu.topology import switches,event


class switchLog(app_manager.RyuApp):

    _CONTEXTS = {'switches': switches.Switches}
    EVENTS = [event.EventSwitchEnter, event.EventSwitchLeave,
               event.EventSwitchReconnected,
               event.EventPortAdd, event.EventPortDelete,
               event.EventPortModify,
               event.EventLinkAdd, event.EventLinkDelete,
               event.EventHostAdd]

    def __init__(self, *args, **kwargs):
        super(switchLog, self).__init__(*args, **kwargs)
        self.name = 'switchLog'

        self.switches = kwargs['switches']
        self.switches._EVENTS=[]

        self.sending_echo_request_interval = 0.05
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)

        # logname='./'+self.name + '.log'
        logname=self.name + '.log'
        # file_name = 'muthu'
        
        # self.logger = self.Logger(file_name)
        # self.logger.basicConfig(filename=logname,
        #                     filemode='a',
        #                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        #                     datefmt='%H:%M:%S',
        #                     level=logging.INFO)
        handler=logging.handlers.WatchedFileHandler(logname)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
   
    
    def Logger(self,file_name):
        formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S') # %I:%M:%S %p AM|PM format
        logging.basicConfig(filename = '%s.log' %(file_name),format= '%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S', filemode = 'w', level = logging.INFO)
        log_obj = logging.getLogger()
        log_obj.setLevel(logging.DEBUG)
        # log_obj = logging.getLogger().addHandler(logging.StreamHandler())

        # console printer
        screen_handler = logging.StreamHandler(stream=sys.stdout) #stream=sys.stdout is similar to normal print
        screen_handler.setFormatter(formatter)
        logging.getLogger().addHandler(screen_handler)

        log_obj.info("Logger object created successfully..")
        return log_obj

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
        self.logger.info('link discovery timeout')

   