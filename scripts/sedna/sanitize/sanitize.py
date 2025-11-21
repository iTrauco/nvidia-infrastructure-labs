#!/usr/bin/env python3
"""Sanitization module - removes sensitive data"""
import json


class Sanitizer:
    def sanitize_entry(self, entry):
        """Sanitize a single chain entry"""
        clean = entry.copy()
        
        # Sanitize hostname
        if "host" in clean:
            hostname = clean["host"].lower()
            if "w32445" in hostname or "zenon" in hostname:
                clean["host"] = "node-001"
            elif "w52445" in hostname or "gemini" in hostname:
                clean["host"] = "node-002"
            elif "control" in hostname:
                clean["host"] = "control"
            else:
                clean["host"] = f"node-{hostname[:4]}"
        
        # Legacy support for 'context' field
        if "context" in clean:
            if "hostname" in clean["context"]:
                hostname = clean["context"]["hostname"].lower()
                if "w32445" in hostname or "zenon" in hostname:
                    clean["context"]["hostname"] = "node-001"
                elif "w52445" in hostname or "gemini" in hostname:
                    clean["context"]["hostname"] = "node-002"
                else:
                    clean["context"]["hostname"] = f"node-{hostname[:4]}"
            if "user" in clean["context"]:
                clean["context"]["user"] = "user"
        
        # Sanitize username
        if "user" in clean:
            clean["user"] = "examprep"
        
        return clean
    
    def sanitize_file(self, input_file="provenance/chain.jsonl", 
                      output_file="provenance/chain_clean.jsonl"):
        """Sanitize entire chain file"""
        with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
            for line in f_in:
                entry = json.loads(line)
                clean_entry = self.sanitize_entry(entry)
                json.dump(clean_entry, f_out)
                f_out.write('\n')
        return output_file


# Test
if __name__ == "__main__":
    sanitizer = Sanitizer()
    test = {"host": "test-hostname", "user": "testuser", "action": "test"}
    print("Original:", test)
    print("Sanitized:", sanitizer.sanitize_entry(test))