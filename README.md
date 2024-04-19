
# Hi, I'm Mohamed Aziz Jlassi ! 👋


## 🚀 About Me

*I'm a Django Backend Developer, always willing to learn and contribute to innovative projects. My key passion is Machine Learning & Deep Learning, where I seek to solve complex problems. I'm interested in collaborating with others on LinkedIn in these topics.*








#  Little Lemon Restaurant
We will create a fully functioning API project for the `Little Lemon Restaurant` so that the client application developers can use the APIs to develop web and mobile applications. People with different roles will be able to browse, add and edit menu items, place orders, browse orders, assign delivery crew to orders and finally deliver the orders. 

### User Groups

 - Manager

 - Delivery crew

 - Customer



## Acknowledgements


The appropriate HTTP status codes for specific errors.



| HTTP Status code |  Reason                       |
| :-------- |  :-------------------------------- |
| `200 - Ok`      |  For all successful  `GET`, `PUT`, `PATCH` and `DELETE` calls |
| `201 - Created` |  For all successful `POST` requests |
| `403 - Unauthorized` |  If authorization fails for the current user token|
| `401 – Forbidden` | If user authentication fails |
| `400 – Bad request` | If validation fails for `POST`, `PUT`, `PATCH` and `DELETE` calls |
| `404 – Not found` | If the request was made for a non-existing resource |




We use Djoser Library in our project to automatically create the following endpoints and functionalities fro user registration and token generation endpoints .






| Endpoint | Role          | Method     | Description                |
| :-------- | :------- | :--------           | :------------------------- |
| `/api/users` | No role required | `POST`        | Creates a new user with name, email and password |
|  `api/users/users/me/` | Anyone with a valid user token | `GET`          | Displays only the current user |
| `/token/login/` | Anyone with a valid credendials| `POST`  | Generates access tokens that can be used in other API calls in this project |

 
Djoser will create other useful endpoints,you can check it [here](https://djoser.readthedocs.io/en/latest/getting_started.html#available-endpoints) .





## API Reference



###  Menu-items Endpoints
 

| GET | POST |
| :-------- | :------- |

```http
/api/items/
```

| GET | PUT | DELETE |
| :-------- | :------- | :------- |


```http
/api/items/${id}
```



### User group management Endpoints

 - ###  Manager 


| GET | POST |
| :-------- | :------- |

```http
/api/manager/users/
```

| GET | PUT | DELETE |
| :-------- | :------- | :------- |

```http
/api/manager/users/${id}
```

| GET | POST |
| :-------- | :------- |

- ###  Delivery Crew 

```http
/api/delivery-crew/users/
```

| GET | PUT | DELETE |
| :-------- | :------- | :------- |

```http
/api/delivery-crew/users/${id}
```


### Cart management Endpoints 

| GET | POST | DELETE |
| :-------- | :------- | :----------|

```http
/api/carts/menu-items/
```



### Order management Endpoints


| GET | POST |
| :-------- | :------- |

```http
/api/orders/
```
| GET | POST | DELETE |
| :-------- | :------- | :----------|

```http
/api/orders/${id}
```



### Categories management Endpoints


| GET | POST |
| :-------- | :------- |

```http
/api/categories/
```
| GET | POST | DELETE |
| :-------- | :------- | :----------|

```http
/api/categories/${id}
```




### Tokens management Endpoints


| POST |
| :-------- | 

```http
/api/token/
```

| POST |
| :-------- | 

```http
/api/token/refresh/
```

| POST |
| :-------- | 

```http
/api/token/blacklist/
```


## 🛠 Skills
- ### `Django` 
- ###  `DjangoRestFramework` 
-  ###  `Djoser` 
-  ###  `APIDevelopement` 
-  ###  ` Backend Developement`


 
 

## 🔗 Links

## LinkedIn : [Jlassi Mohamed Aziz](https://www.linkedin.com/in/mohamed-aziz-jlassi/)
## Gmail : [azizjlassi498@gmail.com](azizjlassi498@gmail.com)





