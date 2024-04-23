// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.31.0
// 	protoc        v4.24.4
// source: cache.proto

package cache

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type ReadObjectRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Digest string `protobuf:"bytes,1,opt,name=digest,proto3" json:"digest,omitempty"`
}

func (x *ReadObjectRequest) Reset() {
	*x = ReadObjectRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_cache_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *ReadObjectRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*ReadObjectRequest) ProtoMessage() {}

func (x *ReadObjectRequest) ProtoReflect() protoreflect.Message {
	mi := &file_cache_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use ReadObjectRequest.ProtoReflect.Descriptor instead.
func (*ReadObjectRequest) Descriptor() ([]byte, []int) {
	return file_cache_proto_rawDescGZIP(), []int{0}
}

func (x *ReadObjectRequest) GetDigest() string {
	if x != nil {
		return x.Digest
	}
	return ""
}

type ReadObjectResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Data []byte `protobuf:"bytes,1,opt,name=data,proto3" json:"data,omitempty"`
}

func (x *ReadObjectResponse) Reset() {
	*x = ReadObjectResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_cache_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *ReadObjectResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*ReadObjectResponse) ProtoMessage() {}

func (x *ReadObjectResponse) ProtoReflect() protoreflect.Message {
	mi := &file_cache_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use ReadObjectResponse.ProtoReflect.Descriptor instead.
func (*ReadObjectResponse) Descriptor() ([]byte, []int) {
	return file_cache_proto_rawDescGZIP(), []int{1}
}

func (x *ReadObjectResponse) GetData() []byte {
	if x != nil {
		return x.Data
	}
	return nil
}

type WriteObjectRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Digest string `protobuf:"bytes,1,opt,name=digest,proto3" json:"digest,omitempty"`
	Data   []byte `protobuf:"bytes,2,opt,name=data,proto3" json:"data,omitempty"`
}

func (x *WriteObjectRequest) Reset() {
	*x = WriteObjectRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_cache_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *WriteObjectRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*WriteObjectRequest) ProtoMessage() {}

func (x *WriteObjectRequest) ProtoReflect() protoreflect.Message {
	mi := &file_cache_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use WriteObjectRequest.ProtoReflect.Descriptor instead.
func (*WriteObjectRequest) Descriptor() ([]byte, []int) {
	return file_cache_proto_rawDescGZIP(), []int{2}
}

func (x *WriteObjectRequest) GetDigest() string {
	if x != nil {
		return x.Digest
	}
	return ""
}

func (x *WriteObjectRequest) GetData() []byte {
	if x != nil {
		return x.Data
	}
	return nil
}

type WriteObjectResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields
}

func (x *WriteObjectResponse) Reset() {
	*x = WriteObjectResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_cache_proto_msgTypes[3]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *WriteObjectResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*WriteObjectResponse) ProtoMessage() {}

func (x *WriteObjectResponse) ProtoReflect() protoreflect.Message {
	mi := &file_cache_proto_msgTypes[3]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use WriteObjectResponse.ProtoReflect.Descriptor instead.
func (*WriteObjectResponse) Descriptor() ([]byte, []int) {
	return file_cache_proto_rawDescGZIP(), []int{3}
}

type HasObjectRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Digest []string `protobuf:"bytes,1,rep,name=digest,proto3" json:"digest,omitempty"`
}

func (x *HasObjectRequest) Reset() {
	*x = HasObjectRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_cache_proto_msgTypes[4]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *HasObjectRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*HasObjectRequest) ProtoMessage() {}

func (x *HasObjectRequest) ProtoReflect() protoreflect.Message {
	mi := &file_cache_proto_msgTypes[4]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use HasObjectRequest.ProtoReflect.Descriptor instead.
func (*HasObjectRequest) Descriptor() ([]byte, []int) {
	return file_cache_proto_rawDescGZIP(), []int{4}
}

func (x *HasObjectRequest) GetDigest() []string {
	if x != nil {
		return x.Digest
	}
	return nil
}

type HasObjectResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Present []bool `protobuf:"varint,1,rep,packed,name=present,proto3" json:"present,omitempty"`
}

func (x *HasObjectResponse) Reset() {
	*x = HasObjectResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_cache_proto_msgTypes[5]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *HasObjectResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*HasObjectResponse) ProtoMessage() {}

func (x *HasObjectResponse) ProtoReflect() protoreflect.Message {
	mi := &file_cache_proto_msgTypes[5]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use HasObjectResponse.ProtoReflect.Descriptor instead.
func (*HasObjectResponse) Descriptor() ([]byte, []int) {
	return file_cache_proto_rawDescGZIP(), []int{5}
}

func (x *HasObjectResponse) GetPresent() []bool {
	if x != nil {
		return x.Present
	}
	return nil
}

var File_cache_proto protoreflect.FileDescriptor

var file_cache_proto_rawDesc = []byte{
	0x0a, 0x0b, 0x63, 0x61, 0x63, 0x68, 0x65, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x12, 0x06, 0x66,
	0x73, 0x74, 0x72, 0x65, 0x65, 0x22, 0x2b, 0x0a, 0x11, 0x52, 0x65, 0x61, 0x64, 0x4f, 0x62, 0x6a,
	0x65, 0x63, 0x74, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x16, 0x0a, 0x06, 0x64, 0x69,
	0x67, 0x65, 0x73, 0x74, 0x18, 0x01, 0x20, 0x01, 0x28, 0x09, 0x52, 0x06, 0x64, 0x69, 0x67, 0x65,
	0x73, 0x74, 0x22, 0x28, 0x0a, 0x12, 0x52, 0x65, 0x61, 0x64, 0x4f, 0x62, 0x6a, 0x65, 0x63, 0x74,
	0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x12, 0x0a, 0x04, 0x64, 0x61, 0x74, 0x61,
	0x18, 0x01, 0x20, 0x01, 0x28, 0x0c, 0x52, 0x04, 0x64, 0x61, 0x74, 0x61, 0x22, 0x40, 0x0a, 0x12,
	0x57, 0x72, 0x69, 0x74, 0x65, 0x4f, 0x62, 0x6a, 0x65, 0x63, 0x74, 0x52, 0x65, 0x71, 0x75, 0x65,
	0x73, 0x74, 0x12, 0x16, 0x0a, 0x06, 0x64, 0x69, 0x67, 0x65, 0x73, 0x74, 0x18, 0x01, 0x20, 0x01,
	0x28, 0x09, 0x52, 0x06, 0x64, 0x69, 0x67, 0x65, 0x73, 0x74, 0x12, 0x12, 0x0a, 0x04, 0x64, 0x61,
	0x74, 0x61, 0x18, 0x02, 0x20, 0x01, 0x28, 0x0c, 0x52, 0x04, 0x64, 0x61, 0x74, 0x61, 0x22, 0x15,
	0x0a, 0x13, 0x57, 0x72, 0x69, 0x74, 0x65, 0x4f, 0x62, 0x6a, 0x65, 0x63, 0x74, 0x52, 0x65, 0x73,
	0x70, 0x6f, 0x6e, 0x73, 0x65, 0x22, 0x2a, 0x0a, 0x10, 0x48, 0x61, 0x73, 0x4f, 0x62, 0x6a, 0x65,
	0x63, 0x74, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x16, 0x0a, 0x06, 0x64, 0x69, 0x67,
	0x65, 0x73, 0x74, 0x18, 0x01, 0x20, 0x03, 0x28, 0x09, 0x52, 0x06, 0x64, 0x69, 0x67, 0x65, 0x73,
	0x74, 0x22, 0x2d, 0x0a, 0x11, 0x48, 0x61, 0x73, 0x4f, 0x62, 0x6a, 0x65, 0x63, 0x74, 0x52, 0x65,
	0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x18, 0x0a, 0x07, 0x70, 0x72, 0x65, 0x73, 0x65, 0x6e,
	0x74, 0x18, 0x01, 0x20, 0x03, 0x28, 0x08, 0x52, 0x07, 0x70, 0x72, 0x65, 0x73, 0x65, 0x6e, 0x74,
	0x32, 0xe1, 0x01, 0x0a, 0x0c, 0x43, 0x61, 0x63, 0x68, 0x65, 0x53, 0x65, 0x72, 0x76, 0x69, 0x63,
	0x65, 0x12, 0x40, 0x0a, 0x09, 0x48, 0x61, 0x73, 0x4f, 0x62, 0x6a, 0x65, 0x63, 0x74, 0x12, 0x18,
	0x2e, 0x66, 0x73, 0x74, 0x72, 0x65, 0x65, 0x2e, 0x48, 0x61, 0x73, 0x4f, 0x62, 0x6a, 0x65, 0x63,
	0x74, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x19, 0x2e, 0x66, 0x73, 0x74, 0x72, 0x65,
	0x65, 0x2e, 0x48, 0x61, 0x73, 0x4f, 0x62, 0x6a, 0x65, 0x63, 0x74, 0x52, 0x65, 0x73, 0x70, 0x6f,
	0x6e, 0x73, 0x65, 0x12, 0x45, 0x0a, 0x0a, 0x52, 0x65, 0x61, 0x64, 0x4f, 0x62, 0x6a, 0x65, 0x63,
	0x74, 0x12, 0x19, 0x2e, 0x66, 0x73, 0x74, 0x72, 0x65, 0x65, 0x2e, 0x52, 0x65, 0x61, 0x64, 0x4f,
	0x62, 0x6a, 0x65, 0x63, 0x74, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x1a, 0x2e, 0x66,
	0x73, 0x74, 0x72, 0x65, 0x65, 0x2e, 0x52, 0x65, 0x61, 0x64, 0x4f, 0x62, 0x6a, 0x65, 0x63, 0x74,
	0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x30, 0x01, 0x12, 0x48, 0x0a, 0x0b, 0x57, 0x72,
	0x69, 0x74, 0x65, 0x4f, 0x62, 0x6a, 0x65, 0x63, 0x74, 0x12, 0x1a, 0x2e, 0x66, 0x73, 0x74, 0x72,
	0x65, 0x65, 0x2e, 0x57, 0x72, 0x69, 0x74, 0x65, 0x4f, 0x62, 0x6a, 0x65, 0x63, 0x74, 0x52, 0x65,
	0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x1b, 0x2e, 0x66, 0x73, 0x74, 0x72, 0x65, 0x65, 0x2e, 0x57,
	0x72, 0x69, 0x74, 0x65, 0x4f, 0x62, 0x6a, 0x65, 0x63, 0x74, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e,
	0x73, 0x65, 0x28, 0x01, 0x42, 0x0b, 0x5a, 0x09, 0x70, 0x6b, 0x67, 0x2f, 0x63, 0x61, 0x63, 0x68,
	0x65, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_cache_proto_rawDescOnce sync.Once
	file_cache_proto_rawDescData = file_cache_proto_rawDesc
)

func file_cache_proto_rawDescGZIP() []byte {
	file_cache_proto_rawDescOnce.Do(func() {
		file_cache_proto_rawDescData = protoimpl.X.CompressGZIP(file_cache_proto_rawDescData)
	})
	return file_cache_proto_rawDescData
}

var file_cache_proto_msgTypes = make([]protoimpl.MessageInfo, 6)
var file_cache_proto_goTypes = []interface{}{
	(*ReadObjectRequest)(nil),   // 0: fstree.ReadObjectRequest
	(*ReadObjectResponse)(nil),  // 1: fstree.ReadObjectResponse
	(*WriteObjectRequest)(nil),  // 2: fstree.WriteObjectRequest
	(*WriteObjectResponse)(nil), // 3: fstree.WriteObjectResponse
	(*HasObjectRequest)(nil),    // 4: fstree.HasObjectRequest
	(*HasObjectResponse)(nil),   // 5: fstree.HasObjectResponse
}
var file_cache_proto_depIdxs = []int32{
	4, // 0: fstree.CacheService.HasObject:input_type -> fstree.HasObjectRequest
	0, // 1: fstree.CacheService.ReadObject:input_type -> fstree.ReadObjectRequest
	2, // 2: fstree.CacheService.WriteObject:input_type -> fstree.WriteObjectRequest
	5, // 3: fstree.CacheService.HasObject:output_type -> fstree.HasObjectResponse
	1, // 4: fstree.CacheService.ReadObject:output_type -> fstree.ReadObjectResponse
	3, // 5: fstree.CacheService.WriteObject:output_type -> fstree.WriteObjectResponse
	3, // [3:6] is the sub-list for method output_type
	0, // [0:3] is the sub-list for method input_type
	0, // [0:0] is the sub-list for extension type_name
	0, // [0:0] is the sub-list for extension extendee
	0, // [0:0] is the sub-list for field type_name
}

func init() { file_cache_proto_init() }
func file_cache_proto_init() {
	if File_cache_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_cache_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*ReadObjectRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_cache_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*ReadObjectResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_cache_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*WriteObjectRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_cache_proto_msgTypes[3].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*WriteObjectResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_cache_proto_msgTypes[4].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*HasObjectRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_cache_proto_msgTypes[5].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*HasObjectResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_cache_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   6,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_cache_proto_goTypes,
		DependencyIndexes: file_cache_proto_depIdxs,
		MessageInfos:      file_cache_proto_msgTypes,
	}.Build()
	File_cache_proto = out.File
	file_cache_proto_rawDesc = nil
	file_cache_proto_goTypes = nil
	file_cache_proto_depIdxs = nil
}
