# stdlib
from collections import defaultdict
from collections import deque
from collections import namedtuple
import threading
import time
from typing import List
from typing import Optional

# third party
from nacl.signing import VerifyKey

# syft absolute
from syft import logger

# syft relative
from .....util import traceback_and_raise
from ...abstract.node import AbstractNode
from ...common.action.smpc_action import SMPCAction
from ...common.service.node_service import ImmediateNodeServiceWithReply
from ...common.service.node_service import ImmediateNodeServiceWithoutReply
from .request_answer_message import RequestAnswerMessage
from .request_answer_message import RequestAnswerResponse
from .request_message import RequestMessage
from .request_message import RequestStatus


class VMRequestService(ImmediateNodeServiceWithoutReply):
    @staticmethod
    def message_handler_types() -> List[type]:
        return [RequestMessage]

    @staticmethod
    def process(
        node: AbstractNode, msg: RequestMessage, verify_key: Optional[VerifyKey] = None
    ) -> None:
        """ """


class VMRequestAnswerMessageService(ImmediateNodeServiceWithReply):
    @staticmethod
    def message_handler_types() -> List[type]:
        return [RequestAnswerMessage]

    @staticmethod
    def process(
        node: AbstractNode,
        msg: RequestAnswerMessage,
        verify_key: Optional[VerifyKey] = None,
    ) -> RequestAnswerResponse:
        if verify_key is None:
            traceback_and_raise(
                ValueError(
                    "Can't process Request service without a given " "verification key"
                )
            )

        status = RequestStatus.Rejected
        address = msg.reply_to
        if node.root_verify_key == verify_key or node.vm_id == address.vm_id:
            status = RequestStatus.Accepted

        return RequestAnswerResponse(
            request_id=msg.request_id, address=address, status=status
        )


actions_lock = threading.Lock()
NodeSMPCAction = namedtuple("NodeSMPCAction", ["node_lock", "smpc_actions"])
actions_to_run_per_node = defaultdict(lambda: NodeSMPCAction(threading.Lock(), deque()))


def consume_smpc_actions_round_robin():
    # Queue keeps a list of actions

    max_nr_retries = 10
    last_msg_id = None
    while True:
        # Get a list of nodes
        with actions_lock:
            nodes = list(actions_to_run_per_node.keys())

        # Get one actions from each node in a Round Robin fashion and try to run it
        for node in nodes:
            with actions_to_run_per_node[node].node_lock:
                if len(actions_to_run_per_node[node].smpc_actions) == 0:
                    continue

                node, msg, verify_key, nr_retries = actions_to_run_per_node[
                    node
                ].smpc_actions[0]
                if nr_retries > max_nr_retries:
                    raise ValueError(f"Retries to many times for {element}")

                try:
                    # try to execute and pop if succeded
                    msg.execute_action(node, verify_key)
                    actions_to_run_per_node[node].smpc_actions.popleft()
                except KeyError:
                    logger.warning(
                        f"Skip SMPC action {msg} since there was a key error when (probably) accessing the store"
                    )

                    if last_msg_id is not None and last_msg_id == msg.id:
                        # If there is only one action in all the lists
                        time.sleep(1)

                last_msg_id = msg.id


thread_smpc_action = threading.Thread(
    target=consume_smpc_actions_round_robin, args=(), daemon=True
)
thread_smpc_action.start()


class VMSMPCService(ImmediateNodeServiceWithoutReply):
    @staticmethod
    def message_handler_types() -> List[type]:
        return [SMPCAction]

    @staticmethod
    def process(
        node: AbstractNode, msg: RequestMessage, verify_key: Optional[VerifyKey] = None
    ) -> None:
        with actions_lock:
            with actions_to_run_per_node[node].node_lock:
                actions_to_run_per_node[node].smpc_actions.append(
                    (node, msg, verify_key, 0)
                )