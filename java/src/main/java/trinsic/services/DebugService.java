// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: DebugService.proto

package trinsic.services;

public final class DebugService {
  private DebugService() {}
  public static void registerAllExtensions(
      com.google.protobuf.ExtensionRegistryLite registry) {
  }

  public static void registerAllExtensions(
      com.google.protobuf.ExtensionRegistry registry) {
    registerAllExtensions(
        (com.google.protobuf.ExtensionRegistryLite) registry);
  }

  public static com.google.protobuf.Descriptors.FileDescriptor
      getDescriptor() {
    return descriptor;
  }
  private static  com.google.protobuf.Descriptors.FileDescriptor
      descriptor;
  static {
    java.lang.String[] descriptorData = {
      "\n\022DebugService.proto\022\020trinsic.services\032\033" +
      "google/protobuf/empty.proto2\211\001\n\tDebuggin" +
      "g\022;\n\tCallEmpty\022\026.google.protobuf.Empty\032\026" +
      ".google.protobuf.Empty\022?\n\rCallEmptyAuth\022" +
      "\026.google.protobuf.Empty\032\026.google.protobu" +
      "f.EmptyB-\n\020trinsic.servicesZ\031github.com/" +
      "trinsic-id/sdkb\006proto3"
    };
    descriptor = com.google.protobuf.Descriptors.FileDescriptor
      .internalBuildGeneratedFileFrom(descriptorData,
        new com.google.protobuf.Descriptors.FileDescriptor[] {
          com.google.protobuf.EmptyProto.getDescriptor(),
        });
    com.google.protobuf.EmptyProto.getDescriptor();
  }

  // @@protoc_insertion_point(outer_class_scope)
}
