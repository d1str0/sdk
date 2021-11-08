# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: services/provider/v1/provider.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import Dict

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase
import grpclib


class ParticipantType(betterproto.Enum):
    participant_type_individual = 0
    participant_type_organization = 1


class InvitationStatusResponseStatus(betterproto.Enum):
    Error = 0
    InvitationSent = 1
    Completed = 2


@dataclass(eq=False, repr=False)
class InviteRequest(betterproto.Message):
    participant: "ParticipantType" = betterproto.enum_field(1)
    description: str = betterproto.string_field(2)
    email: str = betterproto.string_field(5, group="contact_method")
    phone: str = betterproto.string_field(6, group="contact_method")
    didcomm_invitation: "InviteRequestDidCommInvitation" = betterproto.message_field(
        7, group="contact_method"
    )


@dataclass(eq=False, repr=False)
class InviteRequestDidCommInvitation(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class InviteResponse(betterproto.Message):
    status: "__common_v1__.ResponseStatus" = betterproto.enum_field(1)
    invitation_id: str = betterproto.string_field(10)


@dataclass(eq=False, repr=False)
class InvitationStatusRequest(betterproto.Message):
    """
    Request details for the status of onboarding an individual or organization.
    The referenece_id passed is the response from the `Onboard` method call
    """

    invitation_id: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class InvitationStatusResponse(betterproto.Message):
    status: "InvitationStatusResponseStatus" = betterproto.enum_field(1)
    status_details: str = betterproto.string_field(2)


class ProviderStub(betterproto.ServiceStub):
    async def invite(
        self,
        *,
        participant: "ParticipantType" = None,
        description: str = "",
        email: str = "",
        phone: str = "",
        didcomm_invitation: "InviteRequestDidCommInvitation" = None,
    ) -> "InviteResponse":

        request = InviteRequest()
        request.participant = participant
        request.description = description
        request.email = email
        request.phone = phone
        if didcomm_invitation is not None:
            request.didcomm_invitation = didcomm_invitation

        return await self._unary_unary(
            "/services.provider.v1.Provider/Invite", request, InviteResponse
        )

    async def invite_with_workflow(
        self,
        *,
        participant: "ParticipantType" = None,
        description: str = "",
        email: str = "",
        phone: str = "",
        didcomm_invitation: "InviteRequestDidCommInvitation" = None,
    ) -> "InviteResponse":

        request = InviteRequest()
        request.participant = participant
        request.description = description
        request.email = email
        request.phone = phone
        if didcomm_invitation is not None:
            request.didcomm_invitation = didcomm_invitation

        return await self._unary_unary(
            "/services.provider.v1.Provider/InviteWithWorkflow", request, InviteResponse
        )

    async def invitation_status(
        self, *, invitation_id: str = ""
    ) -> "InvitationStatusResponse":

        request = InvitationStatusRequest()
        request.invitation_id = invitation_id

        return await self._unary_unary(
            "/services.provider.v1.Provider/InvitationStatus",
            request,
            InvitationStatusResponse,
        )


class ProviderBase(ServiceBase):
    async def invite(
        self,
        participant: "ParticipantType",
        description: str,
        email: str,
        phone: str,
        didcomm_invitation: "InviteRequestDidCommInvitation",
    ) -> "InviteResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def invite_with_workflow(
        self,
        participant: "ParticipantType",
        description: str,
        email: str,
        phone: str,
        didcomm_invitation: "InviteRequestDidCommInvitation",
    ) -> "InviteResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def invitation_status(self, invitation_id: str) -> "InvitationStatusResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_invite(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "participant": request.participant,
            "description": request.description,
            "email": request.email,
            "phone": request.phone,
            "didcomm_invitation": request.didcomm_invitation,
        }

        response = await self.invite(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_invite_with_workflow(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "participant": request.participant,
            "description": request.description,
            "email": request.email,
            "phone": request.phone,
            "didcomm_invitation": request.didcomm_invitation,
        }

        response = await self.invite_with_workflow(**request_kwargs)
        await stream.send_message(response)

    async def __rpc_invitation_status(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "invitation_id": request.invitation_id,
        }

        response = await self.invitation_status(**request_kwargs)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/services.provider.v1.Provider/Invite": grpclib.const.Handler(
                self.__rpc_invite,
                grpclib.const.Cardinality.UNARY_UNARY,
                InviteRequest,
                InviteResponse,
            ),
            "/services.provider.v1.Provider/InviteWithWorkflow": grpclib.const.Handler(
                self.__rpc_invite_with_workflow,
                grpclib.const.Cardinality.UNARY_UNARY,
                InviteRequest,
                InviteResponse,
            ),
            "/services.provider.v1.Provider/InvitationStatus": grpclib.const.Handler(
                self.__rpc_invitation_status,
                grpclib.const.Cardinality.UNARY_UNARY,
                InvitationStatusRequest,
                InvitationStatusResponse,
            ),
        }


from ...common import v1 as __common_v1__