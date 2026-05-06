# User Flows — Practice Software Testing

---

## 1. Guest — Browse & Search Products

1. Open https://practicesoftwaretesting.com
2. Browse product grid on homepage (all products).
3. Filter by category from the sidebar.
4. Search by keyword using the search bar.
5. Click a product → product detail page (name, price, description, specs, related products).

**Can do without login:** browse, search, view product detail, add to cart.
**Cannot do without login:** favourites, checkout completion, order history.

---

## 2. User Registration

1. Click **Sign In** → navigate to `/auth/login`.
2. Click **Register** link → `/auth/register`.
3. Fill: first name, last name, email, password (+ confirm), address fields.
4. Submit → account created → redirected to login or home.

**Edge cases:**
- Duplicate email → validation error.
- Weak/mismatched password → form error.

---

## 3. User Login

1. Navigate to `/auth/login`.
2. Enter email + password.
3. Submit → receive Bearer token → stored in app state.
4. If 2FA enabled → prompted for TOTP code.

**Error cases:**
- Wrong credentials → 401.
- Locked account → 423.
- Disabled account → 403.

---

## 4. Full Checkout (Authenticated)

### Step 1 — Cart
1. On product page, click **Add to Cart**.
2. Cart icon updates with item count.
3. Click cart icon → cart overview.
4. Adjust quantities or remove items.

### Step 2 — Login Check
- If not logged in → redirected to login → returns to checkout after auth.

### Step 3 — Address
1. Fill shipping address (first name, last name, address, city, state, country, postcode).
2. Form validation runs on each field.
3. Postcode can be looked up via `/postcode-lookup`.
4. Click **Proceed** → only allowed when form is valid.

### Step 4 — Payment
1. Select payment method (Bank Transfer / Gift Card / Credit Card / Buy Now Pay Later / Cash on Delivery).
2. Fill required fields for chosen method.
3. Submit → `POST /payment/check` → `POST /invoices`.
4. Order confirmation shown.

---

## 5. View Order History

1. Log in.
2. Navigate to `/account` → **Orders** tab.
3. List of past invoices with status.
4. Click invoice → detail view + option to download PDF.

---

## 6. Manage Favourites (Wishlist)

1. Log in.
2. On product page, click the heart / favourite icon.
3. Navigate to `/account` → **Favourites** tab.
4. Remove item by clicking icon again.

---

## 7. Contact Form (Guest or User)

1. Navigate to `/contact`.
2. Fill name, email, subject, message.
3. Submit → `POST /messages` → confirmation shown.

---

## 8. Admin — Manage Products

1. Log in as admin.
2. Navigate to `/admin`.
3. Go to **Products** section.
4. Create / Edit / Delete products with name, price, stock, category, brand, images, specs.

---

## 9. Admin — Manage Orders

1. Log in as admin.
2. Navigate to `/admin` → **Invoices**.
3. Search/filter orders.
4. Update order status (e.g., pending → shipped → completed).

---

## 10. Admin — View Reports

1. Log in as admin.
2. Navigate to `/admin` → **Reports**.
3. View sales charts: total sales, top products, top categories, customers by country.

---

## 11. Password Reset

1. Navigate to `/auth/login` → click **Forgot Password**.
2. Enter registered email → `POST /users/forgot-password`.
3. Check email → click reset link → set new password.

---

## 12. Change Password (Authenticated)

1. Log in → navigate to `/account` → **Profile**.
2. Enter current password and new password.
3. Submit → `POST /users/change-password`.
