from cryptography import fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='
message = b'gAAAAABdKL2n8MlCGuRqfcpEWUHgZsaSShkkW_zTvjb27sFG_vKiphMcr2Y8xnXTB7-sEXjbOF5i_A-mphXoNBqpNT9I8j81Rda6X8Xi9RjgD6g0dYnf9OI4SS_SmX4-GQuvNy6b5lSHu-gwj3c7sqo0sbSda0CB5pnphwsjYwKCNc5opdSX3qI='


def main():
    f = fernet.Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
