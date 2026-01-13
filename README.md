<a id="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Mini-Library is a simple management application that allows:

**Admin:**
- Create users
- Add, edit and soft-delete books, authors and rentals
- View all rentals
- Mark rentals as returned

**User:**
- Create rentals
- View available books and authors


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started
    
Follow the instructions below to run the project locally.

### Built With

 - Python
 - Docker
 - FastAPI
 - PostgreSQL
 - SQLAlchemy
 - Alembic
 - JWT (Json Web Token) authentication
 - pwdlib for password hashing
 - Pytest
 - Makefile

### Prerequisites

Software you need to install in order to run the program:

 - Docker
 - Make 

### Installation

1. Clone the repository
   ```sh
   git clone git@github.com:dawidw-km/Mini-Library.git
   ```
2. Set up environment variables
    Copy `.env_example` to `.env` and fill in your data.  

3. Make sure Docker is running, then run:
   ```sh
    cd Mini-Library
    make full-build
    ```
    This command builds Docker images and starts the application stack.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

After starting the application, open the API documentation at:

http://localhost:8000/docs

Use the available endpoints to create users, books, authors and rentals.

The database is empty on first run except for a default admin user.  
You can log in with:

login: `admin`  
password: `admin`

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Dawid Więcław  - dawidwieclaw@hotmail.com

Project Link: [https://github.com/dawidw-km/Mini-Library](https://github.com/dawidw-km/Mini-Library)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
