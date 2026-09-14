# Python Broker Gateway
#
# Owns all connectivity to Alpaca (auth, REST orders, WebSocket market data
# and trade-update streams). Never bypassed by the C++ core — see
# docs/decisions/0001-no-cpp-alpaca-sdk.md.
