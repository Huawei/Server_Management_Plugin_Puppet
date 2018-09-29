type Rest::SnmpTrapServer = Struct[{
  Optional[enabled] => Boolean,
  Optional[port]    => Integer[1, 65535],
  Optional[address] => String,
}]