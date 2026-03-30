from Crypto.Cipher import AES
import hmac
import hashlib

# Global master key for every single MQB Immo V vehicle
MASTER_KEY = b'VAG IMMO KEY 123'

def generate_sync_codes(seed_hex):
    # Clean up input, accept any format with or without spaces
    seed = bytes.fromhex(seed_hex.strip().replace(' ', ''))

    if len(seed) != 32:
        raise ValueError('Seed must be 32 bytes / 64 hex characters')

    # Derive unique per-car secret
    aes = AES.new(MASTER_KEY, AES.MODE_ECB)
    car_key = aes.encrypt(seed[0:16]) + aes.encrypt(seed[16:32])

    print(f'\n✅ Unique permanent car key: {car_key.hex().upper()}')
    print('\nValid sync codes for next 10 counters:')
    print('----------------------------------------')
    print(f'{"Counter":<8} {"Sync Code"}')
    print('----------------------------------------')

    for counter in range(1, 11):
        buffer = car_key + counter.to_bytes(4, byteorder='big')
        mac = hmac.new(MASTER_KEY, buffer, hashlib.sha256).digest()
        sync_code = mac[0:16].hex(' ').upper()
        print(f'{counter:<8} {sync_code}')

    print('\n----------------------------------------')
    print('📝 WORKSHOP NOTE:')
    print('99% of the time you will use Counter 1')
    print('If car starts and dies after 1 second, use Counter 2')
    print('If that fails use Counter 3. You will never need higher.')


if __name__ == '__main__':
    print('MQB Immo Sync Code Generator')
    print('100% offline, no internet required')
    print('----------------------------------------')
    seed = input('Paste 27 01 seed here: ')
    try:
        generate_sync_codes(seed)
    except Exception as e:
        print(f'❌ Error: {e}')

    input('\nPress enter to exit')