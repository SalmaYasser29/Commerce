# CS50 Web Programming with Python and JavaScript
## Project 2: Commerce

### Description
This project is an eBay-like auction site built with Django. Users can create listings, place bids, add comments, manage their watchlist, browse categories, and close auctions. Administrators can manage all data through the Django admin interface.

### Features
- **User Authentication**: Register, log in, and log out.
- **Create Listing**: Users can create auction listings with title, description, starting bid, optional image, and category.
- **Active Listings Page**: Homepage displays all active listings with title, description, price, and image.
- **Listing Page**: Shows details, current price, comments, and allows bidding, watchlist toggle, and closing auction by owner.
- **Bidding**: Validates bids (must be greater than current highest).
- **Watchlist**: Logged-in users can add/remove items and view their watchlist.
- **Comments**: Logged-in users can post comments on listings.
- **Categories**: List all categories and view active listings per category.
- **Close Auction**: Listing owner can close auction; winner displayed if applicable.
- **Admin Panel**: Manage listings, bids, comments, and users.

### Files
- `auctions/models.py` — Defines models: `User`, `Listing`, `Bid`, `Comment`, `Category`, `Watchlist`.
- `auctions/views.py` — Handles app logic and routes.
- `auctions/templates/auctions/` — HTML templates.
- `auctions/urls.py` — URL routes.
- `commerce/settings.py` — Project settings.

### How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/me50/<yourusername>.git
   cd commerce
2. Install dependencies:
    pip install -r requirements.txt
3. Apply migrations:
    python manage.py migrate
4. Run server:
    python manage.py runserver
5. Access at:
    http://127.0.0.1:8000.

### YouTube:
    Video demo: <https://youtu.be/JgsSLDuJUh4>