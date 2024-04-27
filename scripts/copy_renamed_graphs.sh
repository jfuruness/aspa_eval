#! /bin/bash

# you have to make the staging directory before running this

cp results/shortest_path_export_all_hijack_ETC_CC.png staging/customer_cones.png
cp results/forged_origin_export_all_hijack.png staging/origin_hijack.png
cp results/neighbor_spoofing_hijack.png staging/origin_spoofing_hijack.png
cp results/route_leak_mh.png staging/route_leak_mh_ATTACKER_SUCCESS.png
cp results/route_leak_transit.png staging/route_leak_transit_ATTACKER_SUCCESS.png
cp results/shortest_path_export_all_hijack_ETC.png staging/spea_etc.png
cp results/shortest_path_export_all_hijack_INPUT_CLIQUE.png staging/spea_input_clique.png
cp results/shortest_path_export_all_hijack_10_attackers.png staging/spea_multi.png
cp results/shortest_path_export_all_hijack_1_attackers.png staging/spea.png
