# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-08

### Features

- Add base client and settings for Buda API ([30d90ca](https://github.com/mschiaff/buda-client/commit/30d90ca3312151be2452749c5c3dd8d0f63b071c))
- Implement synchronous and asynchronous clients for Buda API with endpoint definitions ([01c2e43](https://github.com/mschiaff/buda-client/commit/01c2e435474d030d427f73aac647f15e99a00663))
- Add account endpoints and implement 'me' method in sync and async clients ([59185ed](https://github.com/mschiaff/buda-client/commit/59185edcd6f634a4cdd8121a2c086f7043d4810d))
- Define UserInfo and AccountInfo models, and add CurrencyValue class for currency representation ([1da1428](https://github.com/mschiaff/buda-client/commit/1da1428620f4ba9b844551b39b896b292b6f3811))
- Enhance async and sync clients with raw request methods and update endpoint model handling ([78399cc](https://github.com/mschiaff/buda-client/commit/78399cc40707b44f0f6c54b25a939400ecd61b69))
- Add markets method to async and sync clients, enhance market model with additional fields and response parsing ([72b0826](https://github.com/mschiaff/buda-client/commit/72b08269a5e59a72aff8b098d677504cdcdd7db6))
- Implement context manager methods for AsyncBudaClient and BudaClient ([bff1674](https://github.com/mschiaff/buda-client/commit/bff1674f5c93e624a79bd06277c6214a00e9a2a5))
- Update market and ticker models, enhance endpoint methods for async and sync clients ([efb8d43](https://github.com/mschiaff/buda-client/commit/efb8d43b35f83692fbe3ef825efc97998df04db1))
- Add order book endpoints and model to async and sync clients ([f5b1928](https://github.com/mschiaff/buda-client/commit/f5b192883b0b9462f517ff9c30acf8783a23e258))
- Add trades endpoint and model to async and sync clients ([0c7d34e](https://github.com/mschiaff/buda-client/commit/0c7d34eb0e094fe1d1bca8dd2352f51ae3c7f0ad))
- Enhance trades endpoint with optional parameters and update request handling in async and sync clients ([ce3f26a](https://github.com/mschiaff/buda-client/commit/ce3f26ac592f0cb270e7220e25128a9a9b6e457d))
- Add with_auth parameter to _request method and move _raw_request method to the end in async and sync clients ([07ff0d3](https://github.com/mschiaff/buda-client/commit/07ff0d35551a69f714c22452f2cccbe55fcf6e0e))
- Add quotations endpoint and model, update request handling in async and sync clients ([e608d1d](https://github.com/mschiaff/buda-client/commit/e608d1d7aedb17daabee088a12fd620704e52d8b))
- Add PublicAPI class with constructor for BudaClient integration ([42a701e](https://github.com/mschiaff/buda-client/commit/42a701e46acad69c64eb837fcfbb71fedc2acd9d))
- Add ruff as a development dependency and refactor endpoint mixins in the Buda API client ([1b218ad](https://github.com/mschiaff/buda-client/commit/1b218ad317e347fbafa4366c5710d100cfe09676))
- Update authentication handling in BudaClient to conditionally use auth credentials ([317fb79](https://github.com/mschiaff/buda-client/commit/317fb794aea6373f3c46203a4461ddd058510fdf))
- Update _request method in BaseClient to include authenticated parameter ([84de4e5](https://github.com/mschiaff/buda-client/commit/84de4e5a157ef44aeef8fae71dc772360c8f5aae))
- Refactor AsyncBudaClient and AsyncPublicAPI to improve request handling and authentication ([7272fdc](https://github.com/mschiaff/buda-client/commit/7272fdc2d479a1c8b2f707a84d192675e93612b7))
- Add pyright and update ruff configuration in project settings ([0d66374](https://github.com/mschiaff/buda-client/commit/0d6637430bdf99d1dee6c6af0e9492e1c207167c))
- Implement Buda API credentials management with environment and static providers ([a8e3783](https://github.com/mschiaff/buda-client/commit/a8e37836b7edb648236bf5622db9e843499cde69))
- Integrate new credential providers and refactor authentication handling in clients ([0ef753e](https://github.com/mschiaff/buda-client/commit/0ef753ec16288816399ba7f0f3c6a6a44cf08656))
- Implement WebSocket client and channel management for real-time updates ([9152cd7](https://github.com/mschiaff/buda-client/commit/9152cd703ecd6b966d3a1732ebd3374ffd88aaf3))
- Add retry and rate limiting functionality to Buda client ([e39dd04](https://github.com/mschiaff/buda-client/commit/e39dd0487b1517ad62761b2da3699dffe5e60df7))
- Enhance BudaSettings with WebSocket API configurations and improve WebSocket client connection handling ([ee1599a](https://github.com/mschiaff/buda-client/commit/ee1599a8842e0c62a9bb43ddb5f70660b6e8c346))
- Add user agent header to WebSocket client connection settings ([617f5a6](https://github.com/mschiaff/buda-client/commit/617f5a61a913fa22c6e8d50d24c40efa305d87ee))
- Add pytest and pytest-asyncio to development dependencies ([1f7260c](https://github.com/mschiaff/buda-client/commit/1f7260c63689ebe0e4ee7748f641b3911509eb83))
- Implement synchronous and asynchronous clients for Buda API ([2a596bd](https://github.com/mschiaff/buda-client/commit/2a596bdbee483556079e6670545a5f588542e13d))
- Implement Buda API client with synchronous and asynchronous support ([e4df0a8](https://github.com/mschiaff/buda-client/commit/e4df0a8d870036cefea116fb38599bf03c542627))
- Add Apache License 2.0 to the project ([77d4b5a](https://github.com/mschiaff/buda-client/commit/77d4b5a537ce276f71bace8d724c3cffbfc3979d))
- Add contributing guidelines to enhance community collaboration ([c2a3774](https://github.com/mschiaff/buda-client/commit/c2a37745d83ab143f3b563471a74d37987c233f5))
- Add close method to BudaClient and AsyncBudaClient for proper resource management ([6e95400](https://github.com/mschiaff/buda-client/commit/6e954006ca263a2c90b3a0df0a4e8105368c2fbb))
- Add raw request tests for AsyncBudaClient and BudaClient ([d365016](https://github.com/mschiaff/buda-client/commit/d3650169cd5faad5457978bcc4152b3bb71a90d5))
- Add tests for default handler and subscribe edge cases in BudaWebSocketClient ([39df27f](https://github.com/mschiaff/buda-client/commit/39df27f9acab4ddabfbbcd26325ec07eb97c61ba))
- Add tests for rate limiter sleep behavior when auth and unauth limits are exceeded ([c0f60fa](https://github.com/mschiaff/buda-client/commit/c0f60fabe89ff090015dcd186e7903cff0e111c0))
- Enhance CI workflow with test result uploads and coverage reporting ([0586ab2](https://github.com/mschiaff/buda-client/commit/0586ab2190f69841409357da19ff39031295a90b))
- Update orders model to use PriceAmountList for bids and asks ([3786cf7](https://github.com/mschiaff/buda-client/commit/3786cf77334ab78ab34c50dfd2a8e72a76b5144b))
- Import deprecated from typing_extensions for compatibility with Python < 3.13 ([b0a694a](https://github.com/mschiaff/buda-client/commit/b0a694a389c7e2cc1846c378c9a86b897eac19d5))
- Add tests for PriceAmountList min and max methods ([3b73ff2](https://github.com/mschiaff/buda-client/commit/3b73ff2b7c37bc363c85826d60b0048a03a219d2))
- Update coverage report configuration to exclude deprecated imports ([ee9d329](https://github.com/mschiaff/buda-client/commit/ee9d329178de66072f012204ac5e3fbf30620283))
- Implement release workflow with version bumping and changelog generation ([c1780dc](https://github.com/mschiaff/buda-client/commit/c1780dcd68ee21d8283ecdd6d895ec43b39ca12c))

### Bug Fixes

- Ensure proper newline at end of file in rate limiter and retry modules ([66864bd](https://github.com/mschiaff/buda-client/commit/66864bd3a89eefea95e2fb473e1c6de914461908))
- Remove unused PING_INTERVAL constant from WebSocket client ([fcc4a86](https://github.com/mschiaff/buda-client/commit/fcc4a860e7edd492a7a03d971034973a81c07a12))
- Reorder imports for better organization in base client ([04ae84e](https://github.com/mschiaff/buda-client/commit/04ae84e95164adfe647bd85ebf9b2526efce4d68))
- Update project description for clarity on API support ([789fc6c](https://github.com/mschiaff/buda-client/commit/789fc6c9ae741e96d36314b43ddb24311c6e8bd3))
- Update GitHub Actions to use latest versions of checkout, setup-uv, and setup-python ([13ca4f5](https://github.com/mschiaff/buda-client/commit/13ca4f504ac43841db3c34f472b42e0d15e6cbc2))
- Update setup-uv cache suffix and upgrade Codecov action to v6 ([d0ddad1](https://github.com/mschiaff/buda-client/commit/d0ddad1605c788d799ce0e737348a611ffe041df))
- Update order book example to use max and min methods for bids and asks ([4381920](https://github.com/mschiaff/buda-client/commit/4381920be040e6bafc109af95fe197f353e8dabe))
- Update project name to 'buda-client' in configuration files ([3f64241](https://github.com/mschiaff/buda-client/commit/3f642411f2c7e4406985f492cb5221151369ac0e))
- Update package name to 'buda-client' in uv.lock and adjust build backend module name in pyproject.toml ([c6150b7](https://github.com/mschiaff/buda-client/commit/c6150b72a178d377dceffbc20b7da8f986b8cfd3))

### Refactor

- Rename SyncBudaClient to BudaClient for consistency ([2643d1a](https://github.com/mschiaff/buda-client/commit/2643d1ab9785dbf3024e6e51441657e90547ca1e))
- Reorganize imports and enhance type hints in client and endpoint modules ([4f1f811](https://github.com/mschiaff/buda-client/commit/4f1f811ba1096ab118a993717d70b7201d04b18b))
- Remove redundant type annotation for HttpxClientType in base.py ([02ad661](https://github.com/mschiaff/buda-client/commit/02ad661accf653277457ecf8684f38b17198b494))
- Reorganize imports and enhance type hints across multiple modules ([3a620b3](https://github.com/mschiaff/buda-client/commit/3a620b368e60bd2acead7bce0aca0dabaf2d8856))
- Clean up imports and remove unused abstract method in base client ([18fe8d0](https://github.com/mschiaff/buda-client/commit/18fe8d070291312bfa65acd6e3c1b97df3dc0096))
- Update .gitignore to include ruff cache and ensure proper formatting ([3f8d4be](https://github.com/mschiaff/buda-client/commit/3f8d4bef6d26ad1513b5e797dc1dbb7314f7df1a))
- Remove unused dependencies from pyproject.toml and uv.lock ([7800dd0](https://github.com/mschiaff/buda-client/commit/7800dd0285390aa29581e1eaaf372dbc40d2f767))
- Streamline imports in async and sync client files ([14d1bc0](https://github.com/mschiaff/buda-client/commit/14d1bc066b03863f946a27d039f8b8c413bac214))
- Update type annotations for HttpxClient and QuotationType ([c2b4e4c](https://github.com/mschiaff/buda-client/commit/c2b4e4c1660cf006a0a74baeb7c7eb05f110ab2a))
- Enhance QuotationParams with NotRequired for limit and adjust type annotations ([88ca8c8](https://github.com/mschiaff/buda-client/commit/88ca8c88c0947bd9358531e38c9f8f476aa4dfe0))
- Rename QuotationParams to QuotationPayload and update related usages ([6462829](https://github.com/mschiaff/buda-client/commit/646282979e330444ca9fcfb1a1c2c86c1a6a10bc))
- Replace string literal with RequestMethod type for method parameter in endpoints ([bba46f2](https://github.com/mschiaff/buda-client/commit/bba46f221bc98ef63d687421dcca328e30cf3f6f))
- Enhance account model with Balance and BalanceList classes, and update endpoint methods ([99bcdcb](https://github.com/mschiaff/buda-client/commit/99bcdcba39b243217c975a9afbe8d80ec96c1a51))
- Enhance order management with OrderCreate and OrderResponse models, and update async/sync clients to support order creation ([8d99c3c](https://github.com/mschiaff/buda-client/commit/8d99c3cc72b9e7082f3272cdbe5a9304713512ea))
- Add OrderDetail model and implement order_detail method in async/sync clients ([0ad134b](https://github.com/mschiaff/buda-client/commit/0ad134b83c6c80086ecb6e6426805a9c75ecb555))
- Update order response models and add cancel order functionality in async/sync clients ([f74ae36](https://github.com/mschiaff/buda-client/commit/f74ae36b0d381723586615a7d7bb733cc448ecdc))
- Implement cancel all orders functionality in async/sync clients and update order models ([f4ab1c4](https://github.com/mschiaff/buda-client/commit/f4ab1c43b5610c6bfeb75cbadf244417b419be84))
- Clean up imports and enhance BudaSettings with base_uri field ([6dfab0a](https://github.com/mschiaff/buda-client/commit/6dfab0af9de41e080de37ff289d0dd7f2765a154))
- Reorganize imports and remove unused base client file ([21d57bf](https://github.com/mschiaff/buda-client/commit/21d57bf5c896c4d8080997908bc61e97b26c43c8))
- Improve docstring clarity in SyncRateLimiter class ([2fbbdbd](https://github.com/mschiaff/buda-client/commit/2fbbdbda0be87bd68b764341d229bd04ae337013))
- Update pyproject.toml for improved structure and clarity ([01a17db](https://github.com/mschiaff/buda-client/commit/01a17db2c929ea4867e10d83ca9308839644d702))

### Styling

- Format code by removing unnecessary blank lines in PriceAmountList methods ([ca5a497](https://github.com/mschiaff/buda-client/commit/ca5a49739546985b3e74052f813bd134800eed94))

### Miscellaneous

- Add initial_tag configuration for versioning ([e953910](https://github.com/mschiaff/buda-client/commit/e9539102381765641732e7f710aa934636b198cf))


