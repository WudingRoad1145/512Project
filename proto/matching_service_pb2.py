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
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'proto/matching_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cproto/matching_service.proto\x12\x08matching\"~\n\x05Order\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x0e\n\x06symbol\x18\x02 \x01(\t\x12\x0c\n\x04side\x18\x03 \x01(\t\x12\r\n\x05price\x18\x04 \x01(\x01\x12\x10\n\x08quantity\x18\x05 \x01(\x01\x12\x11\n\tclient_id\x18\x06 \x01(\t\x12\x11\n\ttimestamp\x18\x07 \x01(\x03\"N\n\x13SubmitOrderResponse\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x15\n\rerror_message\x18\x03 \x01(\t\"D\n\x0b\x46illRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x11\n\tengine_id\x18\x02 \x01(\t\x12\x0f\n\x07timeout\x18\x03 \x01(\x03\"\xd7\x01\n\x0c\x46illResponse\x12\x0f\n\x07\x66ill_id\x18\x01 \x01(\t\x12\x10\n\x08order_id\x18\x02 \x01(\t\x12\x0e\n\x06symbol\x18\x03 \x01(\t\x12\x0c\n\x04side\x18\x04 \x01(\t\x12\r\n\x05price\x18\x05 \x01(\x01\x12\x10\n\x08quantity\x18\x06 \x01(\x01\x12\x1a\n\x12remaining_quantity\x18\x07 \x01(\x01\x12\x11\n\ttimestamp\x18\x08 \x01(\x03\x12\x10\n\x08\x62uyer_id\x18\t \x01(\t\x12\x11\n\tseller_id\x18\n \x01(\t\x12\x11\n\tengine_id\x18\x0b \x01(\t\"9\n\x12\x43\x61ncelOrderRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x11\n\tclient_id\x18\x02 \x01(\t\"N\n\x13\x43\x61ncelOrderResponse\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x15\n\rerror_message\x18\x03 \x01(\t\"0\n\x0bSyncRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x11\n\tengine_id\x18\x02 \x01(\t\"\x95\x01\n\x0fOrderBookUpdate\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\"\n\x04\x62ids\x18\x02 \x03(\x0b\x32\x14.matching.PriceLevel\x12\"\n\x04\x61sks\x18\x03 \x03(\x0b\x32\x14.matching.PriceLevel\x12\x17\n\x0fsequence_number\x18\x04 \x01(\x03\x12\x11\n\tengine_id\x18\x05 \x01(\t\"B\n\nPriceLevel\x12\r\n\x05price\x18\x01 \x01(\x01\x12\x10\n\x08quantity\x18\x02 \x01(\x01\x12\x13\n\x0border_count\x18\x03 \x01(\x05\"%\n\x13GetOrderBookRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\"v\n\tOrderBook\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\"\n\x04\x62ids\x18\x02 \x03(\x0b\x32\x14.matching.PriceLevel\x12\"\n\x04\x61sks\x18\x03 \x03(\x0b\x32\x14.matching.PriceLevel\x12\x11\n\ttimestamp\x18\x04 \x01(\x03\"q\n\x19\x43lientRegistrationRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\x12\x1d\n\x15\x63lient_authentication\x18\x02 \x01(\t\x12\x10\n\x08\x63lient_x\x18\x03 \x01(\x03\x12\x10\n\x08\x63lient_y\x18\x04 \x01(\x03\"J\n\x1a\x43lientRegistrationResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x1c\n\x14match_engine_address\x18\x02 \x01(\t2\xcb\x03\n\x0fMatchingService\x12?\n\x0bSubmitOrder\x12\x0f.matching.Order\x1a\x1d.matching.SubmitOrderResponse\"\x00\x12L\n\x0b\x43\x61ncelOrder\x12\x1c.matching.CancelOrderRequest\x1a\x1d.matching.CancelOrderResponse\"\x00\x12\x45\n\rSyncOrderBook\x12\x15.matching.SyncRequest\x1a\x19.matching.OrderBookUpdate\"\x00\x30\x01\x12\x44\n\x0cGetOrderBook\x12\x1d.matching.GetOrderBookRequest\x1a\x13.matching.OrderBook\"\x00\x12=\n\x08GetFills\x12\x15.matching.FillRequest\x1a\x16.matching.FillResponse\"\x00\x30\x01\x12]\n\x0eRegisterClient\x12#.matching.ClientRegistrationRequest\x1a$.matching.ClientRegistrationResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.matching_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ORDER']._serialized_start=42
  _globals['_ORDER']._serialized_end=168
  _globals['_SUBMITORDERRESPONSE']._serialized_start=170
  _globals['_SUBMITORDERRESPONSE']._serialized_end=248
  _globals['_FILLREQUEST']._serialized_start=250
  _globals['_FILLREQUEST']._serialized_end=318
  _globals['_FILLRESPONSE']._serialized_start=321
  _globals['_FILLRESPONSE']._serialized_end=536
  _globals['_CANCELORDERREQUEST']._serialized_start=538
  _globals['_CANCELORDERREQUEST']._serialized_end=595
  _globals['_CANCELORDERRESPONSE']._serialized_start=597
  _globals['_CANCELORDERRESPONSE']._serialized_end=675
  _globals['_SYNCREQUEST']._serialized_start=677
  _globals['_SYNCREQUEST']._serialized_end=725
  _globals['_ORDERBOOKUPDATE']._serialized_start=728
  _globals['_ORDERBOOKUPDATE']._serialized_end=877
  _globals['_PRICELEVEL']._serialized_start=879
  _globals['_PRICELEVEL']._serialized_end=945
  _globals['_GETORDERBOOKREQUEST']._serialized_start=947
  _globals['_GETORDERBOOKREQUEST']._serialized_end=984
  _globals['_ORDERBOOK']._serialized_start=986
  _globals['_ORDERBOOK']._serialized_end=1104
  _globals['_CLIENTREGISTRATIONREQUEST']._serialized_start=1106
  _globals['_CLIENTREGISTRATIONREQUEST']._serialized_end=1219
  _globals['_CLIENTREGISTRATIONRESPONSE']._serialized_start=1221
  _globals['_CLIENTREGISTRATIONRESPONSE']._serialized_end=1295
  _globals['_MATCHINGSERVICE']._serialized_start=1298
  _globals['_MATCHINGSERVICE']._serialized_end=1757
# @@protoc_insertion_point(module_scope)
