sh = require "stormsh"
sh.start()

heard_reset = false
reset_sock = storm.net.udpsocket(6666, function(msg, ip)
    if not heard_reset then
        heard_reset = true
        storm.os.invokeLater(10*storm.os.SECOND, storm.os.reset)
        cord.new(function()
            for i=1,5 do
                cord.await(storm.os.invokeLater, 1*storm.os.SECOND)
                storm.net.sendto(reset_sock, "RESET", "ff02::1", 6666)
            end
        end)
    end
end)

s = storm.net.udpsocket(4444, function(msg, ip)
    print(string.format("got %s from ip %s", msg, ip))
end)

i = 0
dest = "ip here"
storm.net.clearretrystats()
storm.net.clearroutestats()
function dosend() 
    a = storm.net.retrystats()
    b = storm.net.routestats()

    res = storm.array.fromstr(a)
    pkt_cnt = res:get_as(storm.array.UINT16, 0)
    tx_cnt = res:get_as(storm.array.UINT16_BE, 1)

    res = storm.array.fromstr(b)
    mi_sent = res:get_as(storm.array.UINT8, 0)
    mi_recv = res:get_as(storm.array.UINT8, 1)
    rs_sent = res:get_as(storm.array.UINT8, 2)
    rs_recv = res:get_as(storm.array.UINT8, 3)
    hop_cnt = res:get_as(storm.array.UINT8, 4)

    print(string.format("MI sent/recv: %d/%d RS sent/reccv %d/%d hopcount", mi_sent, mi_recv, rs_sent, rs_recv, hop_cnt))
    pkt = {seq = i, pkt = pkt_cnt, tx = tx_cnt,  mi_sent = mi_sent, mi_recv = mi_recv, rs_sent = rs_sent, rs_recv = rs_recv, hop_cnt = hop_cnt}
    rv = storm.net.sendto(s, storm.mp.pack(pkt), dest, 4444)
    i = i + 1
    storm.net.clearretrystats()
    storm.net.clearroutestats()
end

storm.os.invokePeriodically(10 * storm.os.SECOND, dosend)

cord.enter_loop()
