import random
import numpy as np

# Satellite companies with their service types
companies = [
    ("StarLink Sparkles", "LEO"),
    ("Orbital Ostriches", "GEO"),
    ("Cosmic Cows", "Hybrid"),
    ("Galactic Geckos", "LEO"),
    ("Nebula Narwhals", "GEO"),
    ("Satellite Sloths", "Hybrid"),
    ("Astro Alpacas", "LEO"),
    ("Meteor Meerkats", "GEO"),
    ("Lunar Llamas", "Hybrid"),
    ("Comet Capybaras", "LEO")
]

# Spectrum bands available for auction
# We're using C-band (3.7-4.2 GHz) which has been a focus of recent satellite spectrum auctions
spectrum_blocks = {
    'A': '3.7-3.8 GHz',
    'B': '3.8-3.9 GHz',
    'C': '3.9-4.0 GHz',
    'D': '4.0-4.1 GHz',
    'E': '4.1-4.2 GHz'
}

def generate_valuations():
    """
    Generate random valuations for each company for each spectrum block.
    
    In reality, valuations would depend on factors like the company's current spectrum holdings,
    their technology (GEO/LEO/Hybrid), business plans, and the specific characteristics of each band.
    """
    valuations = {}
    for company, service_type in companies:
        company_valuations = {}
        for block, band in spectrum_blocks.items():
            # LEO operators might value lower frequencies more due to better signal propagation
            # GEO operators might value higher frequencies for higher bandwidth
            # Hybrid operators have balanced valuations
            if service_type == "LEO":
                base_value = random.randint(150, 200) - (ord(block) - ord('A')) * 10
            elif service_type == "GEO":
                base_value = random.randint(150, 200) + (ord(block) - ord('A')) * 10
            else:  # Hybrid
                base_value = random.randint(150, 200)
            
            company_valuations[block] = max(50, min(base_value, 200))  # Ensure values are between 50 and 200
        valuations[(company, service_type)] = company_valuations
    return valuations

def smra(valuations, num_rounds=5):
    """
    Simulate a Simultaneous Multiple Round Auction (SMRA).
    
    SMRA has been widely used in spectrum auctions since the 1990s, including for satellite spectrum.
    The FCC has used this format for various spectrum auctions, including some involving satellite bands.
    
    In SMRA, multiple spectrum blocks are auctioned simultaneously over several rounds.
    Bidders place bids on individual blocks, and the highest bid for each block becomes the standing high bid.
    """
    print("\nSimulating Simultaneous Multiple Round Auction (SMRA)")
    print("This auction type has been widely used by the FCC since the 1990s.")
    
    current_prices = {block: 50 for block in spectrum_blocks}
    allocations = {block: None for block in spectrum_blocks}
    
    for round in range(num_rounds):
        print(f"\nRound {round + 1}")
        bids = {}
        
        for (company, service_type), company_valuations in valuations.items():
            for block in spectrum_blocks:
                if company_valuations[block] >= current_prices[block] and allocations[block] != company:
                    bids.setdefault(block, []).append(company)
        
        for block, bidders in bids.items():
            if bidders:
                winner = random.choice(bidders)
                allocations[block] = winner
                current_prices[block] += 10  # Increment price
            print(f"Block {block} ({spectrum_blocks[block]}): Winner - {allocations[block]}, Price - {current_prices[block]}")
    
    return allocations, current_prices

def cca(valuations):
    """
    Simulate a Combinatorial Clock Auction (CCA).
    
    CCA is a more recent auction format, first used for spectrum in 2008 in the UK.
    It has since been adopted by several countries for spectrum auctions, including for satellite bands.
    
    CCA allows bidders to bid on packages of spectrum, which is particularly useful for satellite
    operators who may need specific combinations of spectrum to operate effectively.
    """
    print("\nSimulating Combinatorial Clock Auction (CCA)")
    print("This auction type has been used since 2008 and allows bidding on spectrum packages.")
    
    current_prices = {block: 50 for block in spectrum_blocks}
    demand = {company: set(spectrum_blocks.keys()) for (company, _) in valuations.keys()}
    
    # Clock phase
    while sum(len(d) for d in demand.values()) > len(spectrum_blocks):
        print("\nClock Phase Round")
        for block in spectrum_blocks:
            bidders = sum(1 for d in demand.values() if block in d)
            if bidders > 1:
                current_prices[block] += 10
            print(f"Block {block} ({spectrum_blocks[block]}): Price - {current_prices[block]}, Demand - {bidders}")
        
        for (company, service_type), company_valuations in valuations.items():
            demand[company] = set(block for block in spectrum_blocks if company_valuations[block] >= current_prices[block])
    
    # Supplementary phase (simplified)
    print("\nSupplementary Phase")
    supplementary_bids = {}
    for (company, service_type), company_valuations in valuations.items():
        package = tuple(sorted(demand[company]))
        bid_value = sum(company_valuations[block] for block in package)
        supplementary_bids[company] = (package, bid_value)
        print(f"{company} ({service_type}): Package {package}, Bid {bid_value}")
    
    # Determine winner (simplified)
    winner = max(supplementary_bids, key=lambda x: supplementary_bids[x][1])
    winning_package, winning_bid = supplementary_bids[winner]
    
    print(f"\nWinner: {winner}")
    print(f"Winning Package: {winning_package}")
    print(f"Winning Bid: {winning_bid}")
    
    return winner, winning_package, winning_bid

def incentive_auction(valuations):
    """
    Simulate a simplified Incentive Auction.
    
    Incentive auctions are a relatively new concept, first used by the FCC in 2017 for repurposing
    broadcast TV spectrum for wireless use. While not yet used for satellite spectrum, this format
    could potentially be applied to repurpose certain satellite bands for terrestrial 5G use.
    
    The auction consists of a reverse auction (existing users selling spectrum back) and a forward
    auction (new users buying the cleared spectrum).
    """
    print("\nSimulating Incentive Auction")
    print("This is a new auction type, first used in 2017 for repurposing broadcast TV spectrum.")
    
    # Forward auction
    forward_result = smra(valuations, num_rounds=3)
    forward_revenue = sum(forward_result[1].values())
    
    # Reverse auction (simplified)
    print("\nReverse Auction")
    clearing_target = random.randint(2, 4)  # Number of blocks to clear
    reverse_bids = {company: random.randint(100, 300) for (company, _) in list(valuations.keys())[:5]}  # Only first 5 companies participate
    sorted_bids = sorted(reverse_bids.items(), key=lambda x: x[1])
    
    cleared_spectrum = sorted_bids[:clearing_target]
    clearing_cost = sum(bid for _, bid in cleared_spectrum)
    
    print(f"Clearing Target: {clearing_target} blocks")
    for company, bid in cleared_spectrum:
        print(f"{company} cleared for {bid}")
    
    net_revenue = forward_revenue - clearing_cost
    print(f"\nForward Auction Revenue: {forward_revenue}")
    print(f"Clearing Cost: {clearing_cost}")
    print(f"Net Revenue: {net_revenue}")
    
    return net_revenue, cleared_spectrum

def sealed_bid_auction(valuations):
    """
    Simulate a Sealed Bid Auction.
    
    Sealed bid auctions have been used for smaller or less contentious spectrum blocks.
    In the satellite industry, they might be used for niche or experimental frequency bands.
    
    In this format, each bidder submits a single bid without knowing the bids of others.
    """
    print("\nSimulating Sealed Bid Auction")
    print("This type is often used for smaller or less contentious spectrum blocks.")
    
    print("\nDebug: Valuations structure:")
    for key, value in valuations.items():
        print(f"{key}: {value}")
    
    bids = {}
    for (company, service_type), company_valuations in valuations.items():
        total_bid = sum(company_valuations.values())
        bids[company] = total_bid
        print(f"Debug: {company} ({service_type}) total bid: {total_bid}")
    
    if not bids:
        print("Error: No bids were calculated. Check the valuations dictionary.")
        return None, None
    
    winner = max(bids, key=bids.get)
    winning_bid = bids[winner]
    
    print("\nBids:")
    for (company, service_type) in valuations.keys():
        print(f"{company} ({service_type}): {bids[company]}")
    
    print(f"\nWinner: {winner}")
    print(f"Winning Bid: {winning_bid}")
    
    return winner, winning_bid

# Run simulations
if __name__ == "__main__":
    valuations = generate_valuations()

    print("Company Valuations for C-band Spectrum Blocks:")
    for (company, service_type), vals in valuations.items():
        print(f"{company} ({service_type}): {vals}")

    smra(valuations)
    cca(valuations)
    incentive_auction(valuations)
    sealed_bid_auction(valuations)