from rest_framework import serializers

from circuits.choices import CircuitStatusChoices
from circuits.models import Provider, Circuit, CircuitTermination, CircuitType
from dcim.api.nested_serializers import NestedCableSerializer, NestedInterfaceSerializer, NestedSiteSerializer
from dcim.api.serializers import CableTerminationSerializer, ConnectedEndpointSerializer
from extras.api.customfields import CustomFieldModelSerializer
from extras.api.serializers import TaggedObjectSerializer
from netbox.api import ChoiceField, ValidatedModelSerializer, WritableNestedSerializer
from tenancy.api.nested_serializers import NestedTenantSerializer
from .nested_serializers import *


#
# Providers
#

class ProviderSerializer(TaggedObjectSerializer, CustomFieldModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuits-api:provider-detail')
    circuit_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Provider
        fields = [
            'id', 'url', 'name', 'slug', 'asn', 'account', 'portal_url', 'noc_contact', 'admin_contact', 'comments', 'tags',
            'custom_fields', 'created', 'last_updated', 'circuit_count',
        ]


#
# Circuits
#

class CircuitTypeSerializer(ValidatedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuits-api:circuittype-detail')
    circuit_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CircuitType
        fields = ['id', 'url', 'name', 'slug', 'description', 'circuit_count']


class CircuitCircuitTerminationSerializer(WritableNestedSerializer, ConnectedEndpointSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuits-api:circuittermination-detail')
    site = NestedSiteSerializer()

    class Meta:
        model = CircuitTermination
        fields = [
            'id', 'url', 'site', 'port_speed', 'upstream_speed', 'xconnect_id', 'connected_endpoint',
            'connected_endpoint_type', 'connected_endpoint_reachable',
        ]


class CircuitSerializer(TaggedObjectSerializer, CustomFieldModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuits-api:circuit-detail')
    provider = NestedProviderSerializer()
    status = ChoiceField(choices=CircuitStatusChoices, required=False)
    type = NestedCircuitTypeSerializer()
    tenant = NestedTenantSerializer(required=False, allow_null=True)
    termination_a = CircuitCircuitTerminationSerializer(read_only=True)
    termination_z = CircuitCircuitTerminationSerializer(read_only=True)

    class Meta:
        model = Circuit
        fields = [
            'id', 'url', 'cid', 'provider', 'type', 'status', 'tenant', 'install_date', 'commit_rate', 'description',
            'termination_a', 'termination_z', 'comments', 'tags', 'custom_fields', 'created', 'last_updated',
        ]


class CircuitTerminationSerializer(CableTerminationSerializer, ConnectedEndpointSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuits-api:circuittermination-detail')
    circuit = NestedCircuitSerializer()
    site = NestedSiteSerializer()
    cable = NestedCableSerializer(read_only=True)

    class Meta:
        model = CircuitTermination
        fields = [
            'id', 'url', 'circuit', 'term_side', 'site', 'port_speed', 'upstream_speed', 'xconnect_id', 'pp_info',
            'description', 'cable', 'cable_peer', 'cable_peer_type', 'connected_endpoint', 'connected_endpoint_type',
            'connected_endpoint_reachable'
        ]
