# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: chat.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import AsyncGenerator, List

import betterproto
import grpclib


@dataclass
class User(betterproto.Message):
    """Specs for the user: the identifier and the logged-in username"""

    id: str = betterproto.string_field(1)
    username: str = betterproto.string_field(2)


@dataclass
class UsernameList(betterproto.Message):
    """Will allow us to print out a list of users"""

    users: List["User"] = betterproto.message_field(1)


@dataclass
class JoinAbility(betterproto.Message):
    """Used for allowing a user to join the chat"""

    error: int = betterproto.int32_field(1)
    success_message: str = betterproto.string_field(2)


@dataclass
class MessageInfo(betterproto.Message):
    """Shows the specs of what will be displayed with a user's chat message"""

    sender: str = betterproto.string_field(1)
    message: str = betterproto.string_field(2)


@dataclass
class BaseMessage(betterproto.Message):
    """This can be empty because we don't have any specs for the messages"""

    pass


class ChatFunctionalityStub(betterproto.ServiceStub):
    async def join_chat(self, *, id: str = "", username: str = "") -> JoinAbility:
        """Takes a user's information; allows a user to join the chat"""

        request = User()
        request.id = id
        request.username = username

        return await self._unary_unary(
            "/grpc.ChatFunctionality/joinChat",
            request,
            JoinAbility,
        )

    async def display_user_list(self) -> UsernameList:
        """Prints out a list of accounts"""

        request = BaseMessage()

        return await self._unary_unary(
            "/grpc.ChatFunctionality/displayUserList",
            request,
            UsernameList,
        )

    async def send_message(self, *, sender: str = "", message: str = "") -> BaseMessage:
        """
        To send a message, you need the 'specs' of what will be displayed
        """

        request = MessageInfo()
        request.sender = sender
        request.message = message

        return await self._unary_unary(
            "/grpc.ChatFunctionality/sendMessage",
            request,
            BaseMessage,
        )

    async def receive_message(self) -> AsyncGenerator[MessageInfo, None]:
        """
        To receive a message, you want to generate a stream of MessageInfo
        entries
        """

        request = BaseMessage()

        async for response in self._unary_stream(
            "/grpc.ChatFunctionality/receiveMessage",
            request,
            MessageInfo,
        ):
            yield response