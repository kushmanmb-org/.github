# zkpdf Repository Setup

This guide provides instructions for cloning and setting up the zkpdf repository from privacy-scaling-explorations.

## Quick Start

To clone and navigate to the zkpdf repository, run the following commands:

```bash
git clone git@github.com:privacy-scaling-explorations/zkpdf
cd zkpdf
```

## Prerequisites

- Git installed on your system
- SSH key configured with your GitHub account (for SSH cloning)
- Alternatively, you can use HTTPS cloning:
  ```bash
  git clone https://github.com/privacy-scaling-explorations/zkpdf.git
  cd zkpdf
  ```

## About zkpdf

The zkpdf repository is maintained by privacy-scaling-explorations and contains tools and utilities for working with zero-knowledge proofs in PDF documents.

## Repository Information

- **Organization**: privacy-scaling-explorations
- **Repository**: zkpdf
- **Clone URL (SSH)**: `git@github.com:privacy-scaling-explorations/zkpdf`
- **Clone URL (HTTPS)**: `https://github.com/privacy-scaling-explorations/zkpdf.git`

## Next Steps

After cloning the repository, refer to the project's README.md file for:
- Installation instructions
- Build and setup procedures
- Usage guidelines
- Contribution guidelines

## Troubleshooting

### SSH Authentication Issues

If you encounter SSH authentication issues:
1. Ensure your SSH key is added to your GitHub account
2. Test your SSH connection: `ssh -T git@github.com`
3. Alternatively, use HTTPS cloning as shown above

### Permission Denied

If you get a "Permission denied" error:
- Use HTTPS cloning instead of SSH
- Or ensure you have the correct access permissions for the repository
