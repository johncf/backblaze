#!/bin/python

import csv
import json
import sys

def key_proc(key):
  return {
    'smart_1_raw': '001R_read_err_rate',
    'smart_1_normalized': '001N_read_err_rate',
    'smart_2_raw': '002R_throughput_perf',
    'smart_2_normalized': '002N_throughput_perf',
    'smart_3_raw': '003R_spinup_time',
    'smart_3_normalized': '003N_spinup_time',
    'smart_4_raw': '004R_start_stop_ct',
    'smart_4_normalized': '004N_start_stop_ct',
    'smart_5_raw': '005R_reallocated_sect_ct',
    'smart_5_normalized': '005N_reallocated_sect_ct',
    'smart_7_raw': '007R_seek_err_rate',
    'smart_7_normalized': '007N_seek_err_rate',
    'smart_8_raw': '008R_seek_time_perf',
    'smart_8_normalized': '008N_seek_time_perf',
    'smart_9_raw': '009R_power_on_hrs',
    'smart_9_normalized': '009N_power_on_hrs',
    'smart_10_raw': '010R_spin_retry_ct',
    'smart_10_normalized': '010N_spin_retry_ct',
    'smart_11_raw': '011R_calibration_retry_ct',
    'smart_11_normalized': '011N_calibration_retry_ct',
    'smart_13_raw': '013R_soft_read_err_rate',
    'smart_13_normalized': '013N_soft_read_err_rate',
    'smart_12_raw': '012R_power_cycle_ct',
    'smart_12_normalized': '012N_power_cycle_ct',
    'smart_22_raw': '022R_helium_level',
    'smart_22_normalized': '022N_helium_level',
    'smart_183_raw': '183R_runtim_badblock_ct',
    'smart_183_normalized': '183N_runtim_badblock_ct',
    'smart_184_raw': '184R_end_to_end_err_ct',
    'smart_184_normalized': '184N_end_to_end_err_ct',
    'smart_187_raw': '187R_uncorrectable_err_ct',
    'smart_187_normalized': '187N_uncorrectable_err_ct',
    'smart_188_raw': '188R_command_timeout',
    'smart_188_normalized': '188N_command_timeout',
    'smart_189_raw': '189R_high_fly_writes',
    'smart_189_normalized': '189N_high_fly_writes',
    'smart_190_raw': '190R_airflow_temp__obs',
    'smart_190_normalized': '190N_temp_diff_100C',
    'smart_191_raw': '191R_g_sense_err_rate',
    'smart_191_normalized': '191N_g_sense_err_rate',
    'smart_192_raw': '192R_power_off_retract_ct',
    'smart_192_normalized': '192N_power_off_retract_ct',
    'smart_193_raw': '193R_load_cycle_ct',
    'smart_193_normalized': '193N_load_cycle_ct',
    'smart_194_raw': '194R_temp_celsius',
    'smart_194_normalized': '194N_temp_celsius',
    'smart_195_raw': '195R_hw_ecc_recovered',
    'smart_195_normalized': '195N_hw_ecc_recovered',
    'smart_196_raw': '196R_reallocation_ev_ct',
    'smart_196_normalized': '196N_reallocation_ev_ct',
    'smart_197_raw': '197R_curr_pending_sect_ct',
    'smart_197_normalized': '197N_curr_pending_sect_ct',
    'smart_198_raw': '198R_uncorrectable_sect_ct',
    'smart_198_normalized': '198N_uncorrectable_sect_ct',
    'smart_199_raw': '199R_crc_err_ct',
    'smart_199_normalized': '199N_crc_err_ct',
    'smart_200_raw': '200R_write_sect_err_rate',
    'smart_200_normalized': '200N_write_sect_err_rate',
    'smart_201_raw': '201R_soft_read_err_rate',
    'smart_201_normalized': '201N_soft_read_err_rate',
    'smart_220_raw': '220R_disk_shift',
    'smart_220_normalized': '220N_disk_shift',
    'smart_222_raw': '222R_loaded_hrs',
    'smart_222_normalized': '222N_loaded_hrs',
    'smart_223_raw': '223R_load_unload_retry_ct',
    'smart_223_normalized': '223N_load_unload_retry_ct',
    'smart_224_raw': '224R_load_friction',
    'smart_224_normalized': '224N_load_friction',
    'smart_225_raw': '225R_load_unload_cycle_ct',
    'smart_225_normalized': '225N_load_unload_cycle_ct',
    'smart_226_raw': '226R_load_in_time',
    'smart_226_normalized': '226N_load_in_time',
    'smart_240_raw': '240R_head_flying_hrs',
    'smart_240_normalized': '240N_head_flying_hrs',
    'smart_241_raw': '241R_lba_write_ct',
    'smart_241_normalized': '241N_lba_write_ct',
    'smart_242_raw': '242R_lba_read_ct',
    'smart_242_normalized': '242N_lba_read_ct',
    'smart_250_raw': '250R_read_err_retry_rate',
    'smart_250_normalized': '250N_read_err_retry_rate',
    'smart_251_raw': '251R_min_spares_remaining',
    'smart_251_normalized': '251N_min_spares_remaining',
    'smart_252_raw': '252R_newly_added_bad_flash_blk',
    'smart_252_normalized': '252N_newly_added_bad_flash_blk',
    'smart_254_raw': '254R_free_fall_protection',
    'smart_254_normalized': '254N_free_fall_protection',
  }.get(key, key)

def json_dump(row):
  clean_row = dict((key_proc(k), v) for k, v in row.items() if v)
  json.dump(clean_row, sys.stdout, sort_keys=True, indent=4)

reader = csv.DictReader(sys.stdin)
sys.stdout.write('[\n')
json_dump(next(reader))
for row in reader:
  sys.stdout.write(',\n')
  json_dump(row)
sys.stdout.write('\n]')
