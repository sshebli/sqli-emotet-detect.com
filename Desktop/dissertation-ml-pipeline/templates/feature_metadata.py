EMOTET_FEATURE_LABELS = {
    "e_conn_count": "Connection Count",
    "e_dns_ratio": "DNS Traffic Ratio",
    "e_http_ratio": "HTTP Traffic Ratio",
    "e_interarrival_std": "Connection Timing Variability",
    "e_mean_duration": "Average Connection Duration",
    "e_mean_orig_bytes": "Average Sent Bytes",
    "e_mean_orig_pkts": "Average Sent Packets",
    "e_mean_resp_bytes": "Average Received Bytes",
    "e_mean_resp_pkts": "Average Received Packets",
    "e_rej_ratio": "Rejected Connection Ratio",
    "e_rst_ratio": "Reset Connection Ratio",
    "e_ssl_ratio": "Encrypted Traffic Ratio",
    "e_std_duration": "Duration Variability",
    "e_tcp_ratio": "TCP Traffic Ratio",
    "e_udp_ratio": "UDP Traffic Ratio",
    "e_unique_dst_ip": "Unique Destination IPs",
    "e_unique_dst_port": "Unique Destination Ports",
}


SQLI_FEATURE_EXPLANATIONS = {
    "Sentence Length": "the total character length of the input. Malicious queries tend to be longer than benign inputs because they append additional clauses, operators, and conditions.",
    "AND count": "the number of times the AND keyword appears. Attackers use AND to inject additional conditions into existing queries, often for boolean-based probing.",
    "OR count": "the number of times OR appears. OR is commonly used in authentication bypass attacks (e.g., OR 1=1) to override restrictive conditions.",
    "UNION count": "the number of times UNION appears. UNION-based injection appends attacker-controlled SELECT statements to extract data from other tables",
    "Single Quote Count": "the number of single quotes ('). Attackers use single quotes to close string literals prematurely and break out of the intended query context.",
    "Double Quote Count": "the number of double quotes, some databases use double quotes for identifiers or string delimitation, and their presence in user input can indicate manipulation.",
    "Constant Value Count": "the number of standalone numeric tokens (e.g., 1, 0, 123). Injection payloads frequently contain numeric literals in logical probes such as 1=1 or 0=0, and in UNION scaffolding such as UNION SELECT 1,2,3.",
    "Parentheses Count": "the number of opening and closing parentheses. Parentheses are used to group injected logical conditions, close existing clauses prematurely, or construct nested expressions.",
    "Special Characters Total": "the total count of non-alphanumeric characters. Malicious inputs tend to be more symbol-dense due to the combination of quotes, operators, comments, and delimiters required for injection.",
}

EMOTET_FEATURE_EXPLANATIONS = {
    "Connection Count": "the total number of connections observed in the window. Infected hosts tend to generate more connections due to C2 check-ins and server cycling.",
    "DNS Traffic Ratio": "the proportion of connections that are DNS queries. Emotet communicates using hardcoded IPs, so DNS activity is unusually low during active C2.",
    "HTTP Traffic Ratio": "the proportion of connections using HTTP.",
    "Connection Timing Variability": "the variability in time gaps between connections. Regular beaconing produces low interarrival variability, while human traffic is irregular.",
    "Average Connection Duration": "the average duration of connections. C2 beaconing produces short, regular connections.",
    "Average Sent Bytes": "the average bytes sent by the host per connection.",
    "Average Sent Packets": "the average number of packets sent per connection.",
    "Average Received Bytes": "the average bytes received per connection.",
    "Average Received Packets": "the average number of packets received per connection. These four features capture the volume profile of each connection. Beaconing traffic typically produces small, consistent packet exchanges.",
    "Rejected Connection Ratio": "the proportion of rejected connections. Elevated rejection rates occur when Emotet cycles through unreachable fallback C2 servers.",
    "Reset Connection Ratio": "the proportion of connections terminated by reset. Abnormal reset rates can indicate failed C2 handshakes or server-side blocking.",
    "Encrypted Traffic Ratio": "the proportion of connections using SSL/TLS encryption.",
    "Duration Variability": "the variability in connection duration. Low variability suggests automated, periodic communication rather than human browsing.",
    "TCP Traffic Ratio": "the proportion of connections using TCP. Emotet C2 communication is predominantly TCP-based.",
    "UDP Traffic Ratio": "the proportion of connections using UDP.",
    "Unique Destination IPs": "the number of distinct external IP addresses contacted. Emotet cycles through multiple C2 servers, producing higher destination diversity than normal browsing.",
    "Unique Destination Ports": "the number of distinct destination ports used. Unusual port diversity can indicate C2 communication on non-standard ports.",
}


def get_feature_display_name(feature_name: str) -> str:
    return EMOTET_FEATURE_LABELS.get(str(feature_name), str(feature_name))


def pretty_feature_group(feature_name):
    sqli_features = {
        "constant value count",
        "parentheses count",
        "average token length",
        "sentence length",
        "single quote count",
        "double quote count",
        "operator count",
        "comment count",
        "hash count",
        "semicolon count",
        "or count",
        "and count",
        "union count",
        "drop count",
        "select count",
        "where count",
        "like count",
        "digit ratio",
        "uppercase ratio",
        "special char ratio",
    }

    if str(feature_name).strip().lower() in sqli_features:
        return "SQLi / Query Syntax"

    return "Emotet / Network"