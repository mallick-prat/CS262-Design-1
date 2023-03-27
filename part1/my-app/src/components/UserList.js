import React from 'react';

const UserList = ({ users }) => {
  return (
    <div>
      {users.map((user, index) => (
        <div key={index}>{user.username}</div>
      ))}
    </div>
  );
};

export default UserList;
