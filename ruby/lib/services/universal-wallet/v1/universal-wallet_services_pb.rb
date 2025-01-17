# Generated by the protocol buffer compiler.  DO NOT EDIT!
# Source: services/universal-wallet/v1/universal-wallet.proto for package 'services.universalwallet.v1'

require 'grpc'
require 'services/universal-wallet/v1/universal-wallet_pb'

module Services
  module Universalwallet
    module V1
      module UniversalWallet
        class Service

          include ::GRPC::GenericService

          self.marshal_class_method = :encode
          self.unmarshal_class_method = :decode
          self.service_name = 'services.universalwallet.v1.UniversalWallet'

          # Retrieve an item from the wallet with a given item identifier
          rpc :GetItem, ::Services::Universalwallet::V1::GetItemRequest, ::Services::Universalwallet::V1::GetItemResponse
          # Search the wallet using a SQL-like syntax
          rpc :Search, ::Services::Universalwallet::V1::SearchRequest, ::Services::Universalwallet::V1::SearchResponse
          # Insert an item into the wallet
          rpc :InsertItem, ::Services::Universalwallet::V1::InsertItemRequest, ::Services::Universalwallet::V1::InsertItemResponse
          # Insert an item into the wallet
          rpc :UpdateItem, ::Services::Universalwallet::V1::UpdateItemRequest, ::Services::Universalwallet::V1::UpdateItemResponse
          # Delete an item from the wallet permanently
          rpc :DeleteItem, ::Services::Universalwallet::V1::DeleteItemRequest, ::Services::Universalwallet::V1::DeleteItemResponse
        end

        Stub = Service.rpc_stub_class
      end
    end
  end
end
