Feature: Product Search, Cart Management and Checkout Business Flow
  As a customer on the Toolshop e-commerce platform
  I want to search for a tool, select it, add it to my shopping cart, and proceed to checkout
  So that I can verify the end-to-end purchasing journey works seamlessly

  @bdd @regression
  Scenario Outline: Complete product search, selection, cart addition and checkout initiation
    Given the user opens the Toolshop home page
    When the user searches for a product with keyword "<keyword>"
    And the user selects the first matching product from the search results
    And the user sets the product quantity to "<quantity>" and adds it to the cart
    And the user navigates to the shopping cart page
    Then the shopping cart should contain a product matching "<keyword>" with total price greater than 0
    And the user proceeds to the checkout step and sees the authentication or billing prompt

    Examples:
      | keyword | quantity |
      | pliers  | 1        |
      | hammer  | 2        |

