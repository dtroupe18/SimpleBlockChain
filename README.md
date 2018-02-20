# SimpleBlockChain
Simple Transaction Blockchain written in Python 3.6 and Flask

## Usage
1. In Terminal type 'python blockchain.py'
* Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)

2. Open Postman

3. You can mine by making a GET request to: localhost:8000/mine
Once you've mined a coin you will get a recipeint id in the response such as "87199569fbf445a5ab904341e0832e2d"

4. You can create a new transaction using by making a POST request to: localhost:8000/transactions/new

  Sample transaction body:
   ```javascript
{
    "sender": "address provided after you mine",
    "recipient": "someone else's address",
    "amount": 5
}
```

5. You can get the full chain by making a GET request to: localhost:8000/chain
 
   Sample Chain:
```javascript
{
    "chain": [{
            "index": 1,
            "previous_hash": 1,
            "proof": 100,
            "timestamp": 1517423660.248161,
            "transactions": []
        },
        {
            "index": 2,
            "previous_hash": "9dc0df1b2e63fa43f2e3c2f3fb9a1d46ad09bd2d0a0ca05c3cec8ef4fc8ea2fa",
            "proof": 41047,
            "timestamp": 1517423704.4156659,
            "transactions": [{
                "amount": 1,
                "recipient": "87199569fbf445a5ab904341e0832e2d",
                "sender": "0"
            }]
        }
    ],
    "length": 2
}
```

You can run the script on multiple machines or change the port number to run two instances on the same machine.
```python
app.run(host='0.0.0.0', port=8000)
app.run(host='0.0.0.0', port=8001)
```
Once you have two or more nodes running you can make a GET request to: localhost:8000/nodes/resolve


