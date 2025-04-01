# Banking Data GraphQL Service

A GraphQL API service for querying bank and branch information, built with FastAPI and Graphene.

## Project Overview

This project provides a GraphQL API that allows users to query information about banks and their branches. The data is stored in a SQLite database and accessed through SQLAlchemy ORM. The GraphQL API is implemented using Graphene and exposed through FastAPI.

## Method Used to Solve the Problem

To create this banking data GraphQL service, I followed these steps:

1. **Database Design**: 
   - Created SQLAlchemy models for Bank and Branch entities
   - Established a one-to-many relationship between banks and branches
   - Set up appropriate primary and foreign keys

2. **Data Loading**:
   - Implemented a startup event handler to load data from CSV
   - Added logic to check for existing data to prevent duplicates
   - Used efficient batch processing for inserting records

3. **GraphQL Schema Implementation**:
   - Used Graphene-SQLAlchemy to create GraphQL types from SQLAlchemy models
   - Implemented connection-based pagination for efficient data retrieval
   - Created resolvers for querying branches with their related bank information

4. **API Development**:
   - Built a FastAPI application to serve the GraphQL endpoint
   - Added support for both GET and POST requests to the GraphQL endpoint
   - Implemented a GraphiQL interface for interactive query testing

5. **Testing**:
   - Created test cases to verify API functionality
   - Tested the GraphQL endpoint with sample queries
   - Ensured proper data relationships were maintained

## Features

- GraphQL API endpoint at `/gql` for querying bank and branch data
- Interactive GraphiQL interface at `/graphiql` for testing queries
- Connection-based pagination for efficient data retrieval
- Relationship mapping between banks and branches
- Automatic data loading from CSV on startup

## Technology Stack

- **FastAPI**: High-performance web framework for building APIs
- **SQLAlchemy**: ORM for database operations
- **Graphene**: GraphQL implementation for Python
- **Graphene-SQLAlchemy**: Integration between Graphene and SQLAlchemy
- **SQLite**: Lightweight database for storing bank and branch data
- **Pytest**: Testing framework for API validation

## Running the Application

The application can be run using uvicorn: `uvicorn app.main:app --reload`
