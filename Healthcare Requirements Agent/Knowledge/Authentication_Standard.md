# Authentication Standard

## Purpose

This standard defines authentication and access-control expectations for applications that provide access to member and claims information.

## Authentication Requirements

1. Users must authenticate before accessing protected member or claims information.

2. Applications must verify the authenticated user before returning sensitive data.

3. Authentication must occur before authorization decisions are made.

4. Authentication failures must not reveal whether a specific member, account, or claim exists.

5. Sessions should expire after a defined period of inactivity.

6. Repeated failed authentication attempts should be logged for security monitoring.

## Authorization Requirements

1. Authentication alone does not grant access to all data.

2. After authentication, the application must verify that the user is authorized to access the requested resource.

3. Members may only access claims and information associated with their own account unless additional authorization has been explicitly granted.

4. Requests for unauthorized resources must be denied.

5. Authorization checks must be performed on the server side and must not rely only on information supplied by the client application.

## Error Handling

Authentication and authorization errors should use clear but non-sensitive messages.

Example:

> Unable to verify access to the requested information.

The application should not expose internal account identifiers, security rules, or system details in authentication error messages.

## Example Business Rule

An authenticated member requesting claim `CLM-10042` must also be verified as the owner of that claim before claim information is returned.
