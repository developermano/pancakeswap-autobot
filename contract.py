from web3 import Web3
from web3.middleware import geth_poa_middleware
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access environment variables
wallet_private_key = os.getenv("wallet_private_key")
wallet_public_key = os.getenv("wallet_public_key")


# Replace with the URL of your BSC node
bsc_node_url = "https://bsc-dataseed.binance.org/"

# Create a Web3 instance
w3 = Web3(Web3.HTTPProvider(bsc_node_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


def get_bnb_balance():
    # Convert balance from wei to BNB
    balance_wei = w3.eth.get_balance(wallet_public_key)
    balance_bnb = w3.from_wei(balance_wei, 'ether')
    return balance_bnb


def make_bet(epoch, bet, amount):
    contract = get_contract()
    if bet == "bear":
        transaction = contract.functions.betBear(epoch).build_transaction(
            {
                "chainId": 56,  # Mainnet
                "gas": 136456,  # Replace with the appropriate gas limit
                "gasPrice": w3.to_wei(3, "gwei"),  # Replace with your desired gas price
                "nonce": w3.eth.get_transaction_count(wallet_public_key),
                "value": w3.to_wei(amount, "ether"),  # The amount you want to bet
            }
        )
    else:
        transaction = contract.functions.betBull(epoch).build_transaction(
            {
                "chainId": 56,  # Mainnet
                "gas": 114545,  # Replace with the appropriate gas limit
                "gasPrice": w3.to_wei(3, "gwei"),  # Replace with your desired gas price
                "nonce": w3.eth.get_transaction_count(wallet_public_key),
                "value": w3.to_wei(amount, "ether"),  # The amount you want to bet
            }
        )
        # Sign the transaction
    signed_transaction = w3.eth.account.sign_transaction(
        transaction, wallet_private_key
    )

    # Send the transaction
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)


def is_bet_win_claimable(epoch):
    contract = get_contract()
    contract_data = contract.functions.claimable(epoch, wallet_public_key).call()
    return contract_data


def claim_winnings(epoch):
    contract = get_contract()
    transaction = contract.functions.claim([epoch]).build_transaction(
        {
            "chainId": 56,  # Mainnet
            "gas": 136456,  # Replace with the appropriate gas limit
            "gasPrice": w3.to_wei(3, "gwei"),  # Replace with your desired gas price
            "nonce": w3.eth.get_transaction_count(wallet_public_key),
        }
    )
    # Sign the transaction
    signed_transaction = w3.eth.account.sign_transaction(
        transaction, wallet_private_key
    )

    # Send the transaction
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)


def get_contract():
    # Replace with the actual contract address
    contract_address = "0x18B2A687610328590Bc8F2e5fEdDe3b582A49cdA"

    # Define the ABI as a list
    contract_abi = [
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_oracleAddress",
                    "type": "address",
                },
                {"internalType": "address", "name": "_adminAddress", "type": "address"},
                {
                    "internalType": "address",
                    "name": "_operatorAddress",
                    "type": "address",
                },
                {
                    "internalType": "uint256",
                    "name": "_intervalSeconds",
                    "type": "uint256",
                },
                {
                    "internalType": "uint256",
                    "name": "_bufferSeconds",
                    "type": "uint256",
                },
                {"internalType": "uint256", "name": "_minBetAmount", "type": "uint256"},
                {
                    "internalType": "uint256",
                    "name": "_oracleUpdateAllowance",
                    "type": "uint256",
                },
                {"internalType": "uint256", "name": "_treasuryFee", "type": "uint256"},
            ],
            "stateMutability": "nonpayable",
            "type": "constructor",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "sender",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "epoch",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "BetBear",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "sender",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "epoch",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "BetBull",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "sender",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "epoch",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "Claim",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "epoch",
                    "type": "uint256",
                },
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "roundId",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "int256",
                    "name": "price",
                    "type": "int256",
                },
            ],
            "name": "EndRound",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "epoch",
                    "type": "uint256",
                },
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "roundId",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "int256",
                    "name": "price",
                    "type": "int256",
                },
            ],
            "name": "LockRound",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "admin",
                    "type": "address",
                }
            ],
            "name": "NewAdminAddress",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "bufferSeconds",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "intervalSeconds",
                    "type": "uint256",
                },
            ],
            "name": "NewBufferAndIntervalSeconds",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "epoch",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "minBetAmount",
                    "type": "uint256",
                },
            ],
            "name": "NewMinBetAmount",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "operator",
                    "type": "address",
                }
            ],
            "name": "NewOperatorAddress",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "oracle",
                    "type": "address",
                }
            ],
            "name": "NewOracle",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "oracleUpdateAllowance",
                    "type": "uint256",
                }
            ],
            "name": "NewOracleUpdateAllowance",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "epoch",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "treasuryFee",
                    "type": "uint256",
                },
            ],
            "name": "NewTreasuryFee",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "previousOwner",
                    "type": "address",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "newOwner",
                    "type": "address",
                },
            ],
            "name": "OwnershipTransferred",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "epoch",
                    "type": "uint256",
                }
            ],
            "name": "Pause",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "account",
                    "type": "address",
                }
            ],
            "name": "Paused",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "epoch",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "rewardBaseCalAmount",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "rewardAmount",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "treasuryAmount",
                    "type": "uint256",
                },
            ],
            "name": "RewardsCalculated",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "epoch",
                    "type": "uint256",
                }
            ],
            "name": "StartRound",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "token",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                },
            ],
            "name": "TokenRecovery",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256",
                }
            ],
            "name": "TreasuryClaim",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "epoch",
                    "type": "uint256",
                }
            ],
            "name": "Unpause",
            "type": "event",
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "account",
                    "type": "address",
                }
            ],
            "name": "Unpaused",
            "type": "event",
        },
        {
            "inputs": [],
            "name": "MAX_TREASURY_FEE",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "adminAddress",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "epoch", "type": "uint256"}],
            "name": "betBear",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "epoch", "type": "uint256"}],
            "name": "betBull",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "bufferSeconds",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint256[]", "name": "epochs", "type": "uint256[]"}
            ],
            "name": "claim",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "claimTreasury",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "epoch", "type": "uint256"},
                {"internalType": "address", "name": "user", "type": "address"},
            ],
            "name": "claimable",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "currentEpoch",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "executeRound",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "genesisLockOnce",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "genesisLockRound",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "genesisStartOnce",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "genesisStartRound",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "user", "type": "address"},
                {"internalType": "uint256", "name": "cursor", "type": "uint256"},
                {"internalType": "uint256", "name": "size", "type": "uint256"},
            ],
            "name": "getUserRounds",
            "outputs": [
                {"internalType": "uint256[]", "name": "", "type": "uint256[]"},
                {
                    "components": [
                        {
                            "internalType": "enum PancakePredictionV2.Position",
                            "name": "position",
                            "type": "uint8",
                        },
                        {
                            "internalType": "uint256",
                            "name": "amount",
                            "type": "uint256",
                        },
                        {"internalType": "bool", "name": "claimed", "type": "bool"},
                    ],
                    "internalType": "struct PancakePredictionV2.BetInfo[]",
                    "name": "",
                    "type": "tuple[]",
                },
                {"internalType": "uint256", "name": "", "type": "uint256"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
            "name": "getUserRoundsLength",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "intervalSeconds",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "", "type": "uint256"},
                {"internalType": "address", "name": "", "type": "address"},
            ],
            "name": "ledger",
            "outputs": [
                {
                    "internalType": "enum PancakePredictionV2.Position",
                    "name": "position",
                    "type": "uint8",
                },
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
                {"internalType": "bool", "name": "claimed", "type": "bool"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "minBetAmount",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "operatorAddress",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "oracle",
            "outputs": [
                {
                    "internalType": "contract AggregatorV3Interface",
                    "name": "",
                    "type": "address",
                }
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "oracleLatestRoundId",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "oracleUpdateAllowance",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "owner",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "pause",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "paused",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "_token", "type": "address"},
                {"internalType": "uint256", "name": "_amount", "type": "uint256"},
            ],
            "name": "recoverToken",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "epoch", "type": "uint256"},
                {"internalType": "address", "name": "user", "type": "address"},
            ],
            "name": "refundable",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "renounceOwnership",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "name": "rounds",
            "outputs": [
                {"internalType": "uint256", "name": "epoch", "type": "uint256"},
                {
                    "internalType": "uint256",
                    "name": "startTimestamp",
                    "type": "uint256",
                },
                {"internalType": "uint256", "name": "lockTimestamp", "type": "uint256"},
                {
                    "internalType": "uint256",
                    "name": "closeTimestamp",
                    "type": "uint256",
                },
                {"internalType": "int256", "name": "lockPrice", "type": "int256"},
                {"internalType": "int256", "name": "closePrice", "type": "int256"},
                {"internalType": "uint256", "name": "lockOracleId", "type": "uint256"},
                {"internalType": "uint256", "name": "closeOracleId", "type": "uint256"},
                {"internalType": "uint256", "name": "totalAmount", "type": "uint256"},
                {"internalType": "uint256", "name": "bullAmount", "type": "uint256"},
                {"internalType": "uint256", "name": "bearAmount", "type": "uint256"},
                {
                    "internalType": "uint256",
                    "name": "rewardBaseCalAmount",
                    "type": "uint256",
                },
                {"internalType": "uint256", "name": "rewardAmount", "type": "uint256"},
                {"internalType": "bool", "name": "oracleCalled", "type": "bool"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "_adminAddress", "type": "address"}
            ],
            "name": "setAdmin",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "_bufferSeconds",
                    "type": "uint256",
                },
                {
                    "internalType": "uint256",
                    "name": "_intervalSeconds",
                    "type": "uint256",
                },
            ],
            "name": "setBufferAndIntervalSeconds",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "_minBetAmount", "type": "uint256"}
            ],
            "name": "setMinBetAmount",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_operatorAddress",
                    "type": "address",
                }
            ],
            "name": "setOperator",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "_oracle", "type": "address"}
            ],
            "name": "setOracle",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "_oracleUpdateAllowance",
                    "type": "uint256",
                }
            ],
            "name": "setOracleUpdateAllowance",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "_treasuryFee", "type": "uint256"}
            ],
            "name": "setTreasuryFee",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "newOwner", "type": "address"}
            ],
            "name": "transferOwnership",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "treasuryAmount",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "treasuryFee",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "unpause",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "address", "name": "", "type": "address"},
                {"internalType": "uint256", "name": "", "type": "uint256"},
            ],
            "name": "userRounds",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
    ]

    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    return contract
