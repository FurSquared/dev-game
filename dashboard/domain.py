from dashboard.models import Token, Reward

def process_csv_codes(reader):
    keys = ['code', 'gm_note', 'reward_text', 'valid_from']
    new_codes = []
    updated_codes = []
    for row in reader:
        valid_from = None if len(row['valid_from']) == 0 else row['valid_from']

        token, created = Token.objects.get_or_create(
            code=row['code'],
            defaults={
                'gm_note': row['gm_note'],
                'reward_text': row['reward_text'],
                'valid_from': valid_from,
            }
        )

        if created:
            new_codes.append(' | '.join([str(getattr(token, key)) for key in keys]))
        else:
            token.gm_note = row['gm_note']
            token.reward_text = row['reward_text']
            token.valid_from = valid_from
            token.save()
            updated_codes.append(' | '.join([str(getattr(token, key)) for key in keys]))

    return (keys, new_codes, updated_codes)

def process_csv_rewards(reader):
    keys = ['name', 'gm_note', 'count', 'required_tokens', 'reward_text', 'valid_from']
    new_rewards = []
    updated_rewards = []
    for row in reader:
        valid_from = None if len(row['valid_from']) == 0 else row['valid_from']
        count = int(row['count']) if len(row['count']) > 0 else 0
        required_tokens = [item.strip() for item in row['required_tokens'].split(',')] if len(row['required_tokens']) > 0 else []

        reward, created = Reward.objects.get_or_create(
            name=row['name'],
            defaults={
                'gm_note': row['gm_note'],
                'reward_text': row['reward_text'],
                'valid_from': valid_from,
                'count': count,
            }
        )

        if created:
            reward.required_tokens.set(required_tokens)
            reward.save()
            new_rewards.append(' | '.join([str(getattr(reward, key)) for key in keys]))
        else:
            reward.gm_note = row['gm_note']
            reward.reward_text = row['reward_text']
            reward.valid_from = valid_from
            reward.count = count
            reward.save()
            updated_rewards.append(' | '.join([str(getattr(reward, key)) for key in keys]))

    return (keys, new_rewards, updated_rewards)
