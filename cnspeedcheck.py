'''
Log measured network bandwidth to JSON logfile

{'client': {
    'rating': '0', 
    'loggedin': '0', 
    'isprating': '3.7', 
    'ispdlavg': '0', 
    'ip': '160.36.13.150', 
    'isp': 'University of Tennessee', 
    'lon': '-83.9622', 
    'ispulavg': '0', 
    'country': 'US', 
    'lat': '35.9901'
    }, 
  'bytes_sent': 142606336, 
  'download': 577075154.6502855, 
  'timestamp': '2018-09-28T14:00:42.731476Z', 
  'share': None, 
  'bytes_received': 409373932, 
  'ping': 72.258, 
  'upload': 452433235.3767918, 
  'server': {
    'latency': 72.258, 
    'name': 'Toronto, ON', 
    'url': 'http://speedtestgta.rogers.com/speedtest/upload.php', 
    'country': 'Canada', 
    'lon': '-79.4042', 
    'cc': 'CA', 
    'host': 'speedtestgta.rogers.com:8080', 
    'sponsor': 'Rogers', 
    'lat': '43.6481', 
    'id': '19249', 
    'd': 935.902020070059
  }
}
'''

import sys
import argparse
import logging
import speedtest
import json

def getNetworkSpeed(servers=[]):
  tester = speedtest.Speedtest()
  logging.info("Check servers...")
  tester.get_servers(servers)
  tester.get_best_server()
  logging.info("Download test...")
  tester.download()
  logging.info("Upload test...")
  tester.upload()
  data = tester.results.dict()
  #flatten the structure
  results = {}
  for k in data['client']:
    results['client_' + k] = data['client'][k]
  for k in data['server']:
    results['server_' + k] = data['server'][k]
  for k in data:
    if k not in ['client', 'server', 'share']:
      results[k] = data[k]
  #Convert bits / sec to MB/s
  results['download'] = data['download'] / 1000.0 / 1000.0 / 8 
  results['upload'] = data['upload'] / 1000.0 / 1000.0 / 8
  results['units'] = "MByte/sec"
  return results

def main():
  parser = argparse.ArgumentParser(description='Network speed test output to JSON.')
  parser.add_argument(
    '-l', '--log_level',
    action='count',
    default=0,
    help='Set logging level, multiples for more detailed.')
  parser.add_argument(
    '-s', '--server',
    default=None,
    help='Specify server to use. speedtest-cli --list for a list.')

  args = parser.parse_args()
  # Setup logging verbosity
  levels = [logging.WARNING, logging.INFO, logging.DEBUG]
  level = levels[min(len(levels) - 1, args.log_level)]
  logging.basicConfig(level=level,
                      format="%(asctime)s %(levelname)s %(message)s")
  servers = []
  if args.server is not None:
    servers.append(int(args.server))
  results = getNetworkSpeed(servers=servers)
  print(json.dumps(results)) #, indent=4, sort_keys=True))
  return 0

if __name__ == "__main__":
  sys.exit(main())
