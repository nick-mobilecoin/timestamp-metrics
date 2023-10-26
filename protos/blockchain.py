# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: blockchain.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto

from . import external
from . import quorum_set as _quorum_set


@dataclass
class BlockID(betterproto.Message):
    """Block ID."""

    data: bytes = betterproto.bytes_field(1)


@dataclass
class BlockContentsHash(betterproto.Message):
    """Hash of the block's contents."""

    data: bytes = betterproto.bytes_field(1)


@dataclass
class Block(betterproto.Message):
    """A block in the blockchain."""

    # Block ID.
    id: "BlockID" = betterproto.message_field(1)
    # Block format version.
    version: int = betterproto.uint32_field(2)
    # Id of the previous block.
    parent_id: "BlockID" = betterproto.message_field(3)
    # The index of this block in the blockchain.
    index: int = betterproto.uint64_field(4)
    # The cumulative number of TXOs in the blockchain, including this block
    cumulative_txo_count: int = betterproto.uint64_field(5)
    # Root hash of the membership proofs provided by the untrusted local system
    # for validation. This captures the state of all TxOuts in the ledger that
    # this block was validated against.
    root_element: external.TxOutMembershipElement = betterproto.message_field(6)
    # Hash of the block's contents.
    contents_hash: "BlockContentsHash" = betterproto.message_field(7)


@dataclass
class BlockContents(betterproto.Message):
    # Key images spent in this block.
    key_images: List[external.KeyImage] = betterproto.message_field(1)
    # Outputs created in this block.
    outputs: List[external.TxOut] = betterproto.message_field(2)
    # / mint-config transactions in this block coupled with data used to validate
    # them.
    validated_mint_config_txs: List[
        external.ValidatedMintConfigTx
    ] = betterproto.message_field(3)
    # / Mint transactions in this block.
    mint_txs: List[external.MintTx] = betterproto.message_field(4)


@dataclass
class BlockSignature(betterproto.Message):
    # The signature of the block.
    signature: external.Ed25519Signature = betterproto.message_field(1)
    # The signer that generated the above signature.
    signer: external.Ed25519Public = betterproto.message_field(2)
    # An approximate time in which the block was signed. Represented as seconds
    # of UTC time since Unix epoch 1970-01-01T00:00:00Z.
    signed_at: int = betterproto.uint64_field(3)


@dataclass
class BlockSignatureData(betterproto.Message):
    # The src_url for the archive block.
    src_url: str = betterproto.string_field(1)
    # The archive filename.
    archive_filename: str = betterproto.string_field(2)
    # The block signature.
    block_signature: BlockSignature = betterproto.message_field(3)


@dataclass
class BlockMetadataContents(betterproto.Message):
    # The Block ID.
    block_id: "BlockID" = betterproto.message_field(1)
    # Quorum set configuration at the time of externalization.
    quorum_set: _quorum_set.QuorumSet = betterproto.message_field(2)
    verification_report: external.VerificationReport = betterproto.message_field(
        3, group="attestation_evidence"
    )
    dcap_evidence: external.DcapEvidence = betterproto.message_field(
        5, group="attestation_evidence"
    )
    # Responder ID of the consensus node that externalized this block.
    responder_id: str = betterproto.string_field(4)


@dataclass
class BlockMetadata(betterproto.Message):
    # Metadata signed by the consensus node.
    contents: "BlockMetadataContents" = betterproto.message_field(1)
    # Message signing key (signer).
    node_key: external.Ed25519Public = betterproto.message_field(2)
    # Signature using `node_key` over the Digestible encoding of `contents`.
    signature: external.Ed25519Signature = betterproto.message_field(3)


@dataclass
class ArchiveBlockV1(betterproto.Message):
    """
    Version 1 of an archived block. Note: The block.version field within the
    block may or may not be equal to 1.
    """

    # The block (header).
    block: "Block" = betterproto.message_field(1)
    # Contents of the block.
    block_contents: "BlockContents" = betterproto.message_field(2)
    # Block signature, when available.
    signature: "BlockSignature" = betterproto.message_field(3)
    # Additional signed metadata about this block.
    metadata: "BlockMetadata" = betterproto.message_field(4)


@dataclass
class ArchiveBlock(betterproto.Message):
    """An archived block."""

    v1: "ArchiveBlockV1" = betterproto.message_field(1, group="block")


@dataclass
class ArchiveBlocks(betterproto.Message):
    """A collection of archived blocks."""

    blocks: List["ArchiveBlock"] = betterproto.message_field(1)
