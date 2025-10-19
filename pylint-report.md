# Pylint report

Here is the Pylint report for the application:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:42:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:48:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:58:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:72:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:79:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:129:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:154:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:176:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:191:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:227:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:238:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:227:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:245:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:255:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:265:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:265:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:292:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:306:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:319:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:345:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:358:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:358:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:393:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:414:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:438:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:447:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:438:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:457:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:2:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module pets
pets.py:1:0: C0114: Missing module docstring (missing-module-docstring)
pets.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:24:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:39:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:39:0: R0913: Too many arguments (6/5) (too-many-arguments)
pets.py:39:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
pets.py:51:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:67:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:67:0: R0913: Too many arguments (6/5) (too-many-arguments)
pets.py:67:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
pets.py:82:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:92:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:97:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:101:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:116:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:129:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:141:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:156:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:160:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:165:0: C0116: Missing function or method docstring (missing-function-docstring)
pets.py:169:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
seed.py:13:0: C0103: Constant name "user_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:14:0: C0103: Constant name "pet_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:15:0: C0103: Constant name "application_count" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:14:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:39:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:43:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:55:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:61:0: C0116: Missing function or method docstring (missing-function-docstring)

-----------------------------------
Your code has been rated at 8.48/10
```

Here is a walkthrough of all the reported issues and arguments for why these remain in the application.

## Module docstring

Majority of the problems are the same type, missing module docstrings:

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
```

These occur because the modules and functions in the application don't have docstrings that explain what each module and function does. Following the course instructions, it was decided not to include docstrings.

## Unnecessary 'else'

Pylint notes two unnecessary usages of ```else``` statements:

```
app.py:238:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:447:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
```

The first case occurs here, in ```delete_pet()```function:

```python
if request.method == "POST":
    check_csrf()
    if "delete" in request.form:
        pets.delete_pet(pet_id)
        return redirect("/")
    else:
        return redirect("/pet/" + str(pet_id))
```

A more concise way to write this section would be to remove ```else``` and de-indent the return statement after it. However, it felt clearer to leave the ```else```, which emphasizes the two possible end results of the code to the reader.

## Inconsistent return statements

Pylint reports these issues in the return statements in functions that handle both ```GET``` and ```POST``` methods:

```
app.py:227:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:265:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:358:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:438:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
```

One example of this is the ```login()``` function:

```python
def login():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("Hold up! Wrong username or password.")
            return redirect("/")
```

The function returns an expression when ```request.method```is either ```GET``` or ```POST```. Technically, if the ```request.method```was something else, the function wouldn't return anything. However, because the decorator specifies the accepted methods to be these two, in reality there is no risk that the function wouldn't return anything.

## Constant naming style

Pylint reported this issue in two files, ```config.py``` and ```seed.py```:

```
config.py:2:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:13:0: C0103: Constant name "user_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:14:0: C0103: Constant name "pet_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:15:0: C0103: Constant name "application_count" doesn't conform to UPPER_CASE naming style (invalid-name)
```

In these case, Pylint views these variables as constants and recommends using the proper naming style of all uppercase letters for them. In both cases, it felt clearer to treat these as variables that might change depending on the situation and therefore follow the variable naming convention. ```config.py```includes also other constants that are named with the correct naming style as they are indeed intended to be high-level shared values (such as character limits and file sizes).

## Dangerous default value

These problems are related to using an empty list ```[]``` as a default value in a function.

```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```

Here is example from the first function that executes database commands:

```python
def execute(sql, params=[]):
    db = get_connection()
    result = db.execute(sql, params)
    db.commit()
    g.last_insert_id = result.lastrowid
    db.close()
```

This could lead to problems if the same empty list was shared between several functions, some of which modified the contents of the list, leading to the changes being reflected in the other functions as well. However, in this case there is no risk of this as these two functions in the app don't modify the contents of the list.

## Too many arguments

Pylin reported these related issues with too many arguments in functions:

```
pets.py:39:0: R0913: Too many arguments (6/5) (too-many-arguments)
pets.py:67:0: R0913: Too many arguments (6/5) (too-many-arguments)
```
```
pets.py:39:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
pets.py:67:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
```

This happens in two functions, which both handle pet information by either adding the data of a new pet to the database or updating it. Here is one of them as an example: 

```python
def update_pet(pet_id, name, birth_year, breed, description, classes):
    sql = """UPDATE pets SET name = ?,
                            birth_year = ?,
                            breed = ?,
                            description = ?
                        WHERE id = ?"""
    db.execute(sql, [name, birth_year, breed, description, pet_id])
```

From developer perspective, it doesn't feel too confusing to have this many arguments for these functions as there are not overly many of them and they relate clearly to the topic of pet entities. However, if there was a need to handle even more pet related data, it could be beneficial to group them into a pet object instead. For this project and its scope, it didn't feel necessary yet.
