# Quick Start - Testing CRUD Functionality

## Getting Started

### 1. Login to Admin Dashboard
```
1. Navigate to: http://localhost:3000/auth/login
2. Enter email and password
3. Click "Sign In"
4. Redirected to: /company-admin/dashboard
```

### 2. Admin Dashboard Layout
```
Header:
├── Title: "Admin Dashboard"
├── 🎨 Brand Settings (button)
└── Logout (button)

Main Content:
├── Messages (success/error appear here)
├── + Add Employee (button)
├── Form (appears when clicked)
└── Employees List (all company employees)
```

## Testing CRUD Operations

### Test 1: CREATE - Add Employee

**Steps:**
1. Click "+ Add Employee" button
2. Form appears with empty fields
3. Fill in fields:
   - Full Name: "Jane Smith" (required)
   - Job Title: "Marketing Manager"
   - Bio: "Creative marketing professional"
   - Photo URL: "https://via.placeholder.com/150"
   - Email: "jane@example.com"
   - Phone: "+1-555-0123"
   - WhatsApp: "+1-555-0124"
   - Instagram: "https://instagram.com/jane"
   - LinkedIn: "https://linkedin.com/in/jane"
   - Facebook: "https://facebook.com/jane"
   - YouTube: "https://youtube.com/@jane"
4. Click "Add Employee" button
5. **Verify:**
   - Green success message appears
   - Form closes automatically
   - "Jane Smith" appears in employee list
   - Success message disappears after 3 seconds

**Test Variations:**
- Add employee with ONLY full name (all other optional)
- Try submitting WITHOUT full name (should be blocked by required field)
- Add employee with empty social links (should be fine)

---

### Test 2: READ - View Employee List

**Steps:**
1. Navigate to admin dashboard
2. Observe employee list

**Verify:**
- Employee name displayed (bold)
- Job title displayed below name (gray)
- Email displayed below job title (gray)
- For each employee:
  - ✏️ Edit button (blue)
  - 🗑️ Delete button (red)
  - 👁️ View button (green)

**Test Variations:**
- With 0 employees: "No employees yet. Add one to get started!"
- With 1+ employees: All displayed in list
- Verify data matches what was entered

---

### Test 3: UPDATE - Edit Employee

**Steps:**
1. Click ✏️ Edit button on any employee
2. **Verify:** Form appears with title "Edit Employee"
3. **Verify:** Form is pre-populated with employee data
4. Modify some fields:
   - Change job title to "Senior Marketing Manager"
   - Change bio to "Updated bio text"
   - Add Instagram URL if missing
5. Click "Update Employee" button
6. **Verify:**
   - Green success message: "Employee updated successfully"
   - Form closes automatically
   - Employee list shows updated data
   - Success message disappears after 3 seconds
7. Click ✏️ Edit again on same employee
8. **Verify:** Form shows all your updates

**Test Variations:**
- Edit only 1 field (leave others)
- Edit social links
- Edit photo URL
- Edit and then click Cancel (form should close without saving)

---

### Test 4: DELETE - Remove Employee

**Steps:**
1. Note an employee name you want to delete
2. Click 🗑️ Delete button on that employee
3. **Verify:** Browser shows confirmation dialog:
   "Are you sure you want to delete this employee?"
4. **Test Option A - Cancel:**
   - Click "Cancel"
   - **Verify:** Dialog closes, employee still in list
5. **Test Option B - Confirm:**
   - Click 🗑️ Delete again on same employee
   - Click "OK" to confirm
   - **Verify:**
     - Red success message: "Employee deleted successfully"
     - Employee removed from list
     - List count decreases
     - Message disappears after 3 seconds

**Test Variations:**
- Delete with 1 employee (should see empty state after)
- Delete middle employee from list
- Delete and refresh page (verify employee stays gone)

---

### Test 5: VIEW - Open Public Card

**Steps:**
1. Click 👁️ View button on any employee
2. **Verify:**
   - New browser tab opens
   - Shows employee digital card
   - URL format: `/card/{company_slug}/{employee_slug}`
   - Card displays:
     - Name (large)
     - Job Title
     - Company Name
     - Bio (if entered)
     - Photo (if entered)
     - Email button (if entered)
     - Phone button (if entered)
     - WhatsApp button (if entered)
     - Download vCard button
     - Social links (with icons)
     - QR Code

3. Back to dashboard tab
4. **Verify:** Employee still in list (View doesn't delete)

---

### Test 6: Form Validation

**Test Required Field:**
1. Click "+ Add Employee"
2. Leave "Full Name" empty
3. Try to click "Add Employee"
4. **Verify:** Form won't submit (browser shows required field message)

**Test Email Validation:**
1. Click "+ Add Employee"
2. Enter "Full Name": "Test User"
3. Enter "Email": "not-an-email"
4. Click "Add Employee"
5. **Verify:** Browser shows email validation message or submits to backend (backend will validate)

---

### Test 7: Error Handling

**Test Network Error:**
1. Open browser DevTools (F12)
2. Click "+ Add Employee"
3. Fill form
4. Open Network tab
5. Right-click request → Block URL or set offline
6. Click "Add Employee"
7. **Verify:** Red error message appears

**Test Authorization Error:**
(Requires manual API testing - beyond UI testing)

---

### Test 8: Success Message Auto-Dismiss

**Steps:**
1. Add an employee
2. **Verify:** Green success message appears
3. **Wait:** Watch for 3 seconds
4. **Verify:** Message automatically disappears
5. No action needed - happens automatically

---

### Test 9: Multiple Operations

**Sequence:**
1. Add employee "Alice Johnson"
2. **Verify:** List shows 1 employee
3. Edit Alice - change job title
4. **Verify:** Updated list shows new title
5. Add employee "Bob Smith"
6. **Verify:** List shows 2 employees
7. Edit Bob - add social links
8. **Verify:** List updates
9. View Alice's card - new tab shows
10. Back to dashboard
11. Delete Bob - confirm
12. **Verify:** List shows only Alice
13. Add Charlie - only name
14. **Verify:** Created successfully

---

## Checking Backend

### Test API Directly (Postman or curl)

**GET Employees:**
```bash
curl -H "Authorization: Bearer {token}" \
  http://localhost:8000/api/company/{company_id}/employees
```

**DELETE Employee:**
```bash
curl -X DELETE -H "Authorization: Bearer {token}" \
  http://localhost:8000/api/employees/{employee_id}
```

**Expected Response:**
```json
{
  "message": "Employee deleted successfully",
  "employee_id": "uuid"
}
```

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Form won't submit | Missing full name | Fill full name field |
| "Not authorized" error | Wrong company or not admin | Verify logged in as admin |
| Employee not deleted | Network error | Check console, try again |
| Form shows old data | Refresh not working | Refresh page manually |
| Social links not showing on card | Empty fields | Make sure URL is filled |
| "Cannot find process" error in editor | TypeScript issue | Ignore - runs fine in Next.js |

---

## Verification Checklist

- [ ] ✅ Create employee with all fields
- [ ] ✅ Create employee with minimal fields
- [ ] ✅ Edit employee - verify form pre-populated
- [ ] ✅ Edit employee - verify changes save
- [ ] ✅ Delete employee - verify confirmation dialog
- [ ] ✅ Delete employee - verify removed from list
- [ ] ✅ View card - opens in new tab
- [ ] ✅ View card - shows all data correctly
- [ ] ✅ Success messages appear and auto-dismiss
- [ ] ✅ Error messages display properly
- [ ] ✅ Form resets after operations
- [ ] ✅ List updates after operations
- [ ] ✅ Mobile responsive (test on phone/tablet)
- [ ] ✅ Can perform multiple operations in sequence

---

## What Should Work

✅ **CREATE**: Add employees with form
✅ **READ**: View list of all employees
✅ **UPDATE**: Edit existing employee data
✅ **DELETE**: Remove employee with confirmation
✅ **VIEW**: Open public card in new tab
✅ **FEEDBACK**: Success/error messages
✅ **VALIDATION**: Required field checking
✅ **MULTI-TENANT**: Only see own company employees

All functionality is now ready to use!
