# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "disk grant-access",
)
class GrantAccess(AAZCommand):
    """Grant a resource access to a managed disk.

    :example: Grant a resource read access to a managed disk.
        az disk grant-access --access-level Read --duration-in-seconds 3600 --name MyManagedDisk --resource-group MyResourceGroup

    :example: Grant a resource read access to a disk to generate access SAS and security data access SAS
        az disk grant-access --access-level Read --duration-in-seconds 3600 --name MyDisk --resource-group MyResourceGroup --secure-vm-guest-state-sas
    """

    _aaz_info = {
        "version": "2023-04-02",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.compute/disks/{}/begingetaccess", "2023-04-02"],
        ]
    }

    AZ_SUPPORT_NO_WAIT = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_lro_poller(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.disk_name = AAZStrArg(
            options=["-n", "--name", "--disk-name"],
            help="The name of the managed disk that is being created. The name can't be changed after the disk is created. Supported characters for the name are a-z, A-Z, 0-9, _ and -. The maximum name length is 80 characters.",
            required=True,
            id_part="name",
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )

        # define Arg Group "GrantAccessData"

        _args_schema = cls._args_schema
        _args_schema.access_level = AAZStrArg(
            options=["--access", "--access-level"],
            arg_group="GrantAccessData",
            help="Access level.",
            required=True,
            default="Read",
            enum={"None": "None", "Read": "Read", "Write": "Write"},
        )
        _args_schema.duration_in_seconds = AAZIntArg(
            options=["--duration-in-seconds"],
            arg_group="GrantAccessData",
            help="Time duration in seconds until the SAS access expires.",
            required=True,
        )
        _args_schema.secure_vm_guest_state_sas = AAZBoolArg(
            options=["-s", "--secure-vm-guest-state-sas"],
            arg_group="GrantAccessData",
            help="Get SAS on managed disk with VM guest state. It will be used by default when the create option of disk is 'secureOSUpload'",
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        yield self.DisksGrantAccess(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class DisksGrantAccess(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200,
                    self.on_error,
                    lro_options={"final-state-via": "location"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200,
                    self.on_error,
                    lro_options={"final-state-via": "location"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/disks/{diskName}/beginGetAccess",
                **self.url_parameters
            )

        @property
        def method(self):
            return "POST"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "diskName", self.ctx.args.disk_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2023-04-02",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Content-Type", "application/json",
                ),
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content_builder(
                self.ctx.args,
                typ=AAZObjectType,
                typ_kwargs={"flags": {"required": True, "client_flatten": True}}
            )
            _builder.set_prop("access", AAZStrType, ".access_level", typ_kwargs={"flags": {"required": True}})
            _builder.set_prop("durationInSeconds", AAZIntType, ".duration_in_seconds", typ_kwargs={"flags": {"required": True}})
            _builder.set_prop("getSecureVMGuestStateSAS", AAZBoolType, ".secure_vm_guest_state_sas")

            return self.serialize_content(_content_value)

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.access_sas = AAZStrType(
                serialized_name="accessSAS",
                flags={"read_only": True},
            )
            _schema_on_200.security_data_access_sas = AAZStrType(
                serialized_name="securityDataAccessSAS",
                flags={"read_only": True},
            )

            return cls._schema_on_200


class _GrantAccessHelper:
    """Helper class for GrantAccess"""


__all__ = ["GrantAccess"]
