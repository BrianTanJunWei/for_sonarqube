import React from 'react';
import { Button, Form, FormGroup, Label, Input } from 'reactstrap';

function PasswordChangeForm({ currentPassword, newPassword, onCurrentPasswordChange, onNewPasswordChange, onSubmit }) {
  return (
    <Form onSubmit={onSubmit}>
      <FormGroup>
        <Label for="currentPassword">Current Password</Label>
        <Input
          type="password"
          id="currentPassword"
          value={currentPassword}
          onChange={onCurrentPasswordChange}
        />
      </FormGroup>
      <FormGroup>
        <Label for="newPassword">New Password</Label>
        <Input
          type="password"
          id="newPassword"
          value={newPassword}
          onChange={onNewPasswordChange}
        />
      </FormGroup>
      <Button color="primary" type="submit">
        Save Changes
      </Button>
    </Form>
  );
}

export default PasswordChangeForm;
