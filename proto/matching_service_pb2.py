# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: proto/matching_service.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 5, 28, 1, "", "proto/matching_service.proto"
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1cproto/matching_service.proto\x12\x08matching"\xbd\x01\n\x0cOrderRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x12\x0c\n\x04side\x18\x03 \x01(\t\x12\r\n\x05price\x18\x04 \x01(\x01\x12\x10\n\x08quantity\x18\x05 \x01(\x03\x12\x1a\n\x12remaining_quantity\x18\x06 \x01(\x03\x12\x11\n\tclient_id\x18\x07 \x01(\t\x12\x1a\n\x12\x65ngine_origin_addr\x18\x08 \x01(\t\x12\x11\n\ttimestamp\x18\t \x01(\x03"N\n\x13SubmitOrderResponse\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x15\n\rerror_message\x18\x03 \x01(\t"R\n\x0b\x46illRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x1f\n\x17\x65ngine_destination_addr\x18\x02 \x01(\t\x12\x0f\n\x07timeout\x18\x03 \x01(\x03"\xdd\x01\n\x04\x46ill\x12\x0f\n\x07\x66ill_id\x18\x01 \x01(\t\x12\x10\n\x08order_id\x18\x02 \x01(\t\x12\x0e\n\x06symbol\x18\x03 \x01(\t\x12\x0c\n\x04side\x18\x04 \x01(\t\x12\r\n\x05price\x18\x05 \x01(\x01\x12\x10\n\x08quantity\x18\x06 \x01(\x03\x12\x1a\n\x12remaining_quantity\x18\x07 \x01(\x03\x12\x11\n\ttimestamp\x18\x08 \x01(\x03\x12\x10\n\x08\x62uyer_id\x18\t \x01(\t\x12\x11\n\tseller_id\x18\n \x01(\t\x12\x1f\n\x17\x65ngine_destination_addr\x18\x0b \x01(\t"A\n\x0ePutFillRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x1c\n\x04\x66ill\x18\x02 \x01(\x0b\x32\x0e.matching.Fill"!\n\x0fPutFillResponse\x12\x0e\n\x06status\x18\x01 \x01(\t"g\n\x12\x43\x61ncelOrderRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x11\n\tclient_id\x18\x02 \x01(\t\x12,\n\x0corder_record\x18\x03 \x01(\x0b\x32\x16.matching.OrderRequest"S\n\x13\x43\x61ncelOrderResponse\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x1a\n\x12quantity_cancelled\x18\x03 \x01(\x03"B\n\nPriceLevel\x12\r\n\x05price\x18\x01 \x01(\x01\x12\x10\n\x08quantity\x18\x02 \x01(\x03\x12\x13\n\x0border_count\x18\x03 \x01(\x05"D\n\x0bSyncRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x11\n\tengine_id\x18\x02 \x01(\t\x12\x12\n\nnum_levels\x18\x03 \x01(\x03"\x92\x01\n\x0cSyncResponse\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12"\n\x04\x62ids\x18\x02 \x03(\x0b\x32\x14.matching.PriceLevel\x12"\n\x04\x61sks\x18\x03 \x03(\x0b\x32\x14.matching.PriceLevel\x12\x17\n\x0fsequence_number\x18\x04 \x01(\x03\x12\x11\n\tengine_id\x18\x05 \x01(\t"\xbf\x01\n\x19\x42roadcastOrderbookRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x1d\n\x15originating_engine_id\x18\x02 \x01(\t\x12\x12\n\nnum_levels\x18\x03 \x01(\x03\x12"\n\x04\x62ids\x18\x04 \x03(\x0b\x32\x14.matching.PriceLevel\x12"\n\x04\x61sks\x18\x05 \x03(\x0b\x32\x14.matching.PriceLevel\x12\x17\n\x0fsequence_number\x18\x06 \x01(\x03"Y\n\x1a\x42roadcastOrderbookResponse\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x1b\n\x13receiving_engine_id\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\t"%\n\x13GetOrderbookRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t"\x81\x01\n\x14GetOrderbookResponse\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12"\n\x04\x62ids\x18\x02 \x03(\x0b\x32\x14.matching.PriceLevel\x12"\n\x04\x61sks\x18\x03 \x03(\x0b\x32\x14.matching.PriceLevel\x12\x11\n\ttimestamp\x18\x04 \x01(\x03"q\n\x19\x43lientRegistrationRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x1d\n\x15\x63lient_authentication\x18\x02 \x01(\t\x12\x10\n\x08\x63lient_x\x18\x03 \x01(\x03\x12\x10\n\x08\x63lient_y\x18\x04 \x01(\x03"J\n\x1a\x43lientRegistrationResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x1c\n\x14match_engine_address\x18\x02 \x01(\t"W\n\x11RegisterMERequest\x12\x11\n\tengine_id\x18\x01 \x01(\t\x12\x13\n\x0b\x65ngine_addr\x18\x02 \x01(\t\x12\x1a\n\x12\x65ngine_credentials\x18\x03 \x01(\t"$\n\x12RegisterMEResponse\x12\x0e\n\x06status\x18\x01 \x01(\t"W\n\x11\x44iscoverMERequest\x12\x11\n\tengine_id\x18\x01 \x01(\t\x12\x13\n\x0b\x65ngine_addr\x18\x02 \x01(\t\x12\x1a\n\x12\x65ngine_credentials\x18\x03 \x01(\t">\n\x12\x44iscoverMEResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x18\n\x10\x65ngine_addresses\x18\x02 \x03(\t2\x8b\x06\n\x0fMatchingService\x12\x46\n\x0bSubmitOrder\x12\x16.matching.OrderRequest\x1a\x1d.matching.SubmitOrderResponse"\x00\x12L\n\x0b\x43\x61ncelOrder\x12\x1c.matching.CancelOrderRequest\x1a\x1d.matching.CancelOrderResponse"\x00\x12@\n\rSyncOrderBook\x12\x15.matching.SyncRequest\x1a\x16.matching.SyncResponse"\x00\x12\x61\n\x12\x42roadcastOrderbook\x12#.matching.BroadcastOrderbookRequest\x1a$.matching.BroadcastOrderbookResponse"\x00\x12O\n\x0cGetOrderBook\x12\x1d.matching.GetOrderbookRequest\x1a\x1e.matching.GetOrderbookResponse"\x00\x12\x35\n\x08GetFills\x12\x15.matching.FillRequest\x1a\x0e.matching.Fill"\x00\x30\x01\x12@\n\x07PutFill\x12\x18.matching.PutFillRequest\x1a\x19.matching.PutFillResponse"\x00\x12]\n\x0eRegisterClient\x12#.matching.ClientRegistrationRequest\x1a$.matching.ClientRegistrationResponse"\x00\x12I\n\nRegisterME\x12\x1b.matching.RegisterMERequest\x1a\x1c.matching.RegisterMEResponse"\x00\x12I\n\nDiscoverME\x12\x1b.matching.DiscoverMERequest\x1a\x1c.matching.DiscoverMEResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "proto.matching_service_pb2", _globals
)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_ORDERREQUEST"]._serialized_start = 43
    _globals["_ORDERREQUEST"]._serialized_end = 232
    _globals["_SUBMITORDERRESPONSE"]._serialized_start = 234
    _globals["_SUBMITORDERRESPONSE"]._serialized_end = 312
    _globals["_FILLREQUEST"]._serialized_start = 314
    _globals["_FILLREQUEST"]._serialized_end = 396
    _globals["_FILL"]._serialized_start = 399
    _globals["_FILL"]._serialized_end = 620
    _globals["_PUTFILLREQUEST"]._serialized_start = 622
    _globals["_PUTFILLREQUEST"]._serialized_end = 687
    _globals["_PUTFILLRESPONSE"]._serialized_start = 689
    _globals["_PUTFILLRESPONSE"]._serialized_end = 722
    _globals["_CANCELORDERREQUEST"]._serialized_start = 724
    _globals["_CANCELORDERREQUEST"]._serialized_end = 827
    _globals["_CANCELORDERRESPONSE"]._serialized_start = 829
    _globals["_CANCELORDERRESPONSE"]._serialized_end = 912
    _globals["_PRICELEVEL"]._serialized_start = 914
    _globals["_PRICELEVEL"]._serialized_end = 980
    _globals["_SYNCREQUEST"]._serialized_start = 982
    _globals["_SYNCREQUEST"]._serialized_end = 1050
    _globals["_SYNCRESPONSE"]._serialized_start = 1053
    _globals["_SYNCRESPONSE"]._serialized_end = 1199
    _globals["_BROADCASTORDERBOOKREQUEST"]._serialized_start = 1202
    _globals["_BROADCASTORDERBOOKREQUEST"]._serialized_end = 1393
    _globals["_BROADCASTORDERBOOKRESPONSE"]._serialized_start = 1395
    _globals["_BROADCASTORDERBOOKRESPONSE"]._serialized_end = 1484
    _globals["_GETORDERBOOKREQUEST"]._serialized_start = 1486
    _globals["_GETORDERBOOKREQUEST"]._serialized_end = 1523
    _globals["_GETORDERBOOKRESPONSE"]._serialized_start = 1526
    _globals["_GETORDERBOOKRESPONSE"]._serialized_end = 1655
    _globals["_CLIENTREGISTRATIONREQUEST"]._serialized_start = 1657
    _globals["_CLIENTREGISTRATIONREQUEST"]._serialized_end = 1770
    _globals["_CLIENTREGISTRATIONRESPONSE"]._serialized_start = 1772
    _globals["_CLIENTREGISTRATIONRESPONSE"]._serialized_end = 1846
    _globals["_REGISTERMEREQUEST"]._serialized_start = 1848
    _globals["_REGISTERMEREQUEST"]._serialized_end = 1935
    _globals["_REGISTERMERESPONSE"]._serialized_start = 1937
    _globals["_REGISTERMERESPONSE"]._serialized_end = 1973
    _globals["_DISCOVERMEREQUEST"]._serialized_start = 1975
    _globals["_DISCOVERMEREQUEST"]._serialized_end = 2062
    _globals["_DISCOVERMERESPONSE"]._serialized_start = 2064
    _globals["_DISCOVERMERESPONSE"]._serialized_end = 2126
    _globals["_MATCHINGSERVICE"]._serialized_start = 2129
    _globals["_MATCHINGSERVICE"]._serialized_end = 2908
# @@protoc_insertion_point(module_scope)
